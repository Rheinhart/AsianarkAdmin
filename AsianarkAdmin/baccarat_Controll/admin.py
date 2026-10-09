# -*- coding: utf-8 -*-
"""游戏业务后台。

与老版本的主要差别（详见 README「改了什么」一节）：

* 删掉了 9 份 `setListPerPage_*`（45 个方法）和 9 处 `request._set_post` hack，
  统一由 `FastPaginationMixin` 提供 `?per_page=25|50|100|200`；
* `list_filter` 不再放高基数字段（loginname / videoid / url / tableid / seats），
  时间字段改用 `RelativeDateFilter`；
* 注单页的合计条改成对 `cl.queryset` 做一次 `aggregate()`，跟随筛选，
  "本页小计"真的只算当前页，且不会除零；
* `save_model` 一律先 `obj.save()`（老代码改视频/改桌台只写 memcache 不写库）；
* 删除通知走 `delete_model/delete_queryset`（框架扩展点），不再自定义删除 action；
* 不再 `del actions['delete_selected']`，改用 `has_delete_permission`；
* 时间列统一走 `badges.dt`（受 settings.TIME_ZONE 控制），金额统一按"分"渲染。
"""
from __future__ import annotations

from django.contrib import admin, messages
from django.db.models import Count, Sum, Value
from django.db.models.functions import Coalesce
from django.utils.html import format_html

from AsianarkAdmin.admin_ext.actions import export_csv
from AsianarkAdmin.admin_ext.badges import badge, cents, choice_badge, dt
from AsianarkAdmin.admin_ext.filters import relative_date_filter
from AsianarkAdmin.admin_ext.pagination import FastPaginationMixin
from AsianarkAdmin.admin_ext.scoping import AgentScopedAdminMixin
from AsianarkAdmin.admin_ext.site import admin_site
from AsianarkAdmin.admin_ext.stats import ChangelistStatsMixin

from . import services
from .forms import TBulletinForm
from .models import (
    TBulletin,
    TOrders,
    TPersonalLimitset,
    TRecalcRounds,
    TRounds,
    TTable,
    TTableLimitset,
    TVideo,
)

OrderDateFilter = relative_date_filter(
    title="创建时间", parameter_name="date_range", field_name="create_time"
)
ReckonDateFilter = relative_date_filter(
    title="结算时间", parameter_name="reckon_range", field_name="reckon_time"
)
RoundDateFilter = relative_date_filter(
    title="开局时间", parameter_name="date_range", field_name="begintime"
)


# ====================================================================== 公告
@admin.register(TBulletin, site=admin_site)
class TBulletinAdmin(FastPaginationMixin, admin.ModelAdmin):
    form = TBulletinForm

    list_display = ("bulletinid", "text_short", "created_cell", "expired_cell", "flag_cell")
    list_display_links = ("bulletinid",)
    search_fields = ("bulletinid", "text")
    list_filter = ("flag",)
    ordering = ("-bulletinid",)
    readonly_fields = ("create_time",)
    list_per_page = 50

    @admin.display(description="公告内容")
    def text_short(self, obj):
        text = obj.text or ""
        return text if len(text) <= 40 else format_html("{}…", text[:40])

    @admin.display(description="创建时间", ordering="create_time")
    def created_cell(self, obj):
        return dt(obj.create_time)

    @admin.display(description="到期时间", ordering="expired_time")
    def expired_cell(self, obj):
        return dt(obj.expired_time)

    @admin.display(description="状态", ordering="flag")
    def flag_cell(self, obj):
        return choice_badge(obj, "flag")


# ====================================================================== 视频
@admin.register(TVideo, site=admin_site)
class TVideoAdmin(FastPaginationMixin, admin.ModelAdmin):
    list_display = ("videoid", "gametype", "bettime", "url", "flag_cell", "tables_cell")
    list_display_links = ("videoid",)
    search_fields = ("videoid", "url")
    # 老配置把 videoid / bettime / url / flag 全塞进 list_filter：
    # 每个字段都会对全表 DISTINCT 并渲染一个下拉框，url 和 bettime 根本没有过滤意义。
    list_filter = ("gametype", "flag")
    ordering = ("videoid",)
    list_per_page = 50
    actions = ("repush", "export_csv")

    def get_queryset(self, request):
        # 一次 annotate 代替每行一次 ttable_set.count()（N+1）
        return super().get_queryset(request).annotate(_tables=Count("ttable"))

    def get_readonly_fields(self, request, obj=None):
        # 新增时主键必须可填，编辑时锁死
        return ("videoid",) if obj else ()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        obj.save()  # ← 老代码在 change 分支只写 memcache，不写数据库
        services.sync_video(obj)
        if not services.push_video(obj, created=not change):
            self.message_user(
                request,
                "已保存，但通知游戏服失败（已加入重试队列，可用 manage.py flush_push_queue 重放）。",
                messages.WARNING,
            )

    # 删除通知走框架扩展点，不再自己写一个"删除所选并通知"的 action
    def delete_model(self, request, obj):
        obj.delete()
        services.push_videos_deleted([obj.videoid])

    def delete_queryset(self, request, queryset):
        videoids = list(queryset.values_list("videoid", flat=True))
        queryset.delete()
        services.push_videos_deleted(videoids)

    @admin.action(description="📡 重新推送所选视频到游戏服")
    def repush(self, request, queryset):
        ok = sum(1 for obj in queryset if services.push_video(obj, created=False))
        self.message_user(request, f"已推送 {ok} 个视频，失败 {queryset.count() - ok} 个（详见日志）。")

    @admin.display(description="状态", ordering="flag")
    def flag_cell(self, obj):
        return choice_badge(obj, "flag")

    @admin.display(description="引用桌台")
    def tables_cell(self, obj):
        count = getattr(obj, "_tables", 0)
        return badge(f"{count} 张", "warn" if count else "muted")


# ====================================================================== 桌台
@admin.register(TTable, site=admin_site)
class TTableAdmin(FastPaginationMixin, admin.ModelAdmin):
    list_display = ("tableid", "videoid", "gametype", "limitid", "seats", "flag_cell")
    list_display_links = ("tableid",)
    list_select_related = ("videoid",)
    autocomplete_fields = ("videoid",)
    search_fields = ("tableid", "videoid__videoid")
    list_filter = ("gametype", "flag", "limitid")
    ordering = ("tableid",)
    list_per_page = 50
    actions = ("repush", "export_csv")

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        obj.save()  # ← 同上：老代码编辑桌台不写库
        services.sync_table(obj)
        if not services.push_table(obj, created=not change):
            self.message_user(
                request,
                "已保存，但通知游戏服失败（已加入重试队列）。",
                messages.WARNING,
            )

    def delete_model(self, request, obj):
        obj.delete()
        services.push_table(obj, created=False)

    @admin.action(description="📡 重新推送所选桌台到游戏服")
    def repush(self, request, queryset):
        ok = sum(1 for obj in queryset if services.push_table(obj, created=False))
        self.message_user(request, f"已推送 {ok} 张桌台，失败 {queryset.count() - ok} 张。")

    @admin.display(description="状态", ordering="flag")
    def flag_cell(self, obj):
        return choice_badge(obj, "flag")


# ====================================================================== 限红
@admin.register(TTableLimitset, site=admin_site)
class TTableLimitsetAdmin(FastPaginationMixin, admin.ModelAdmin):
    list_display = ("limitid", "playtype", "min_cents_cell", "max_cents_cell", "flag_cell")
    search_fields = ("limitid",)
    list_filter = ("flag", "playtype")
    list_per_page = 50

    @admin.display(description="最小下注额")
    def min_cents_cell(self, obj):
        return cents(obj.min_cents)

    @admin.display(description="最大下注额")
    def max_cents_cell(self, obj):
        return cents(obj.max_cents)

    @admin.display(description="状态", ordering="flag")
    def flag_cell(self, obj):
        return choice_badge(obj, "flag")


@admin.register(TPersonalLimitset, site=admin_site)
class TPersonalLimitsetAdmin(TTableLimitsetAdmin):
    pass


# ====================================================================== 注单
@admin.register(TOrders, site=admin_site)
class TOrdersAdmin(AgentScopedAdminMixin, FastPaginationMixin, ChangelistStatsMixin, admin.ModelAdmin):
    list_display = (
        "billno",
        "loginname",
        "gametype",
        "tableid",
        "seat",
        "dealer",
        "flag_cell",
        "bet_cell",
        "valid_cell",
        "win_cell",
        "credit_change",
        "created_cell",
        "reckoned_cell",
    )
    list_display_links = ("billno",)
    # 老配置把 create_time / reckon_time 放进 search_fields → 对时间列做 __icontains，全表扫描。
    search_fields = ("=billno", "loginname", "roundcode", "tableid", "dealer")
    search_help_text = "注单号（精确）、账户名、局号、桌台、荷官"
    list_filter = ("flag", "gametype", OrderDateFilter, ReckonDateFilter)
    list_per_page = 50
    count_probe_rows = 5000
    actions = (export_csv,)

    readonly_fields = tuple(field.name for field in TOrders._meta.fields)

    # 合计跟随筛选；本页小计只算当前页
    stats_specs = [
        {"key": "count", "label": "注单数", "expr": Count("billno"), "fmt": "int"},
        {
            "key": "bet",
            "label": "投注额",
            "expr": Coalesce(Sum("bet_amount_cents"), Value(0)),
            "fmt": "cents",
        },
        {
            "key": "valid",
            "label": "有效投注额",
            "expr": Coalesce(Sum("valid_bet_amount_cents"), Value(0)),
            "fmt": "cents",
        },
        {
            "key": "win",
            "label": "玩家盈利",
            "expr": Coalesce(Sum("win_amount_cents"), Value(0)),
            "fmt": "cents_signed",
        },
    ]
    stats_ratio = {"key": "rate", "label": "盈利率", "num": "win", "den": "valid", "scale": 100, "fmt": "pct"}
    page_specs = [
        {"key": "bet", "label": "投注额", "field": "bet_amount_cents", "fmt": "cents"},
        {"key": "valid", "label": "有效投注额", "field": "valid_bet_amount_cents", "fmt": "cents"},
        {"key": "win", "label": "玩家盈利", "field": "win_amount_cents", "fmt": "cents_signed"},
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="结算标志", ordering="flag")
    def flag_cell(self, obj):
        return choice_badge(obj, "flag", kind_map={0: "warn", 1: "ok", 8: "vip", -1: "muted"})

    @admin.display(description="投注额", ordering="bet_amount_cents")
    def bet_cell(self, obj):
        return cents(obj.bet_amount_cents)

    @admin.display(description="有效投注额", ordering="valid_bet_amount_cents")
    def valid_cell(self, obj):
        return cents(obj.valid_bet_amount_cents)

    @admin.display(description="盈利额", ordering="win_amount_cents")
    def win_cell(self, obj):
        return cents(obj.win_amount_cents, signed=True)

    @admin.display(description="额度变化")
    def credit_change(self, obj):
        return format_html(
            '<span class="quiet">{}</span> → <b>{}</b>',
            f"{obj.before_credit_cents / 100:,.2f}",
            f"{obj.after_credit_cents / 100:,.2f}",
        )

    @admin.display(description="创建时间", ordering="create_time")
    def created_cell(self, obj):
        return dt(obj.create_time)

    @admin.display(description="结算时间", ordering="reckon_time")
    def reckoned_cell(self, obj):
        return dt(obj.reckon_time)


# ====================================================================== 游戏局
@admin.register(TRounds, site=admin_site)
class TRoundAdmin(FastPaginationMixin, admin.ModelAdmin):
    list_display = (
        "roundcode",
        "gametype",
        "videoid",
        "dealer",
        "flag_cell",
        "points",
        "cards",
        "cardnum",
        "pair_cell",
        "shoecode",
        "begin_cell",
        "close_cell",
    )
    list_display_links = ("roundcode",)
    search_fields = ("roundcode", "dealer", "shoecode", "videoid")
    search_help_text = "局号、荷官、靴号、视频ID"
    list_filter = ("flag", "gametype", "videoid", RoundDateFilter)
    ordering = ("-roundcode",)
    list_per_page = 50
    actions = ("recalc_rounds", "cancel_rounds")

    # cards 允许人工补录（老代码把它注释掉了，结果只能靠游戏服）
    readonly_fields = (
        "roundcode",
        "gametype",
        "videoid",
        "dealer",
        "flag",
        "cardnum",
        "pair",
        "bankerpoint",
        "playerpoint",
        "begintime",
        "closetime",
        "shoecode",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.save()
        if change and obj.flag == 0:
            if not services.recalc_round(obj.roundcode, obj.cards or ""):
                self.message_user(request, "已保存，但重新结算指令发送失败（已加入重试队列）。", messages.WARNING)

    @admin.action(description="🎲 重新结算所选局")
    def recalc_rounds(self, request, queryset):
        self._round_command(request, queryset, services.recalc_round, "重新结算", settled_text="已结算成功", skip_text="已结算过的局已跳过")

    @admin.action(description="⛔ 取消所选局的注单结算")
    def cancel_rounds(self, request, queryset):
        self._round_command(request, queryset, services.cancel_round, "取消结算", settled_text="取消成功", skip_text="未结算的局已跳过")

    def _round_command(self, request, queryset, command, verb, settled_text, skip_text):
        # 重新结算只针对未结算(flag=0)的局；取消只针对已结算的局
        if command is services.recalc_round:
            targets = queryset.filter(flag=0)
        else:
            targets = queryset.exclude(flag=0)
        skipped = queryset.count() - targets.count()

        ok = 0
        for round_obj in targets:
            if command(round_obj.roundcode, getattr(round_obj, "cards", "") or ""):
                ok += 1
                self.log_change(request, round_obj, f"{verb}: {settled_text}")
        parts = [f"{verb}：{ok} 局{settled_text}"]
        if skipped:
            parts.append(f"{skipped} 局{skip_text}")
        if ok < targets.count():
            parts.append(f"{targets.count() - ok} 局发送失败（已进重试队列）")
        self.message_user(request, "；".join(parts))

    @admin.display(description="结算标志", ordering="flag")
    def flag_cell(self, obj):
        return choice_badge(obj, "flag")

    @admin.display(description="庄/闲")
    def points(self, obj):
        return format_html("<b>{}</b> : <b>{}</b>", obj.bankerpoint, obj.playerpoint)

    @admin.display(description="庄闲对", ordering="pair")
    def pair_cell(self, obj):
        return choice_badge(obj, "pair") if obj.pair is not None else badge("—", "muted")

    @admin.display(description="开始时间", ordering="begintime")
    def begin_cell(self, obj):
        return dt(obj.begintime)

    @admin.display(description="结束时间", ordering="closetime")
    def close_cell(self, obj):
        return dt(obj.closetime)


# ====================================================================== 重新结算记录
@admin.register(TRecalcRounds, site=admin_site)
class TRecalcRoundsAdmin(FastPaginationMixin, admin.ModelAdmin):
    list_display = ("actionid", "action", "roundcode", "created_cell")
    search_fields = ("actionid", "action", "roundcode")
    list_filter = ("action", relative_date_filter(
        title="操作时间", parameter_name="date_range", field_name="create_time"
    ))
    ordering = ("-actionid",)
    list_per_page = 50

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="创建时间", ordering="create_time")
    def created_cell(self, obj):
        return dt(obj.create_time)
