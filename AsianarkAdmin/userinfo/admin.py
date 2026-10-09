# -*- coding: utf-8 -*-
"""客户 / 流水 / 代理后台。

主要修复：
* `TAgentsAdmin.save_model` 老代码写的是 `TAgents.create_ip = ip`（给**类的字段描述符**赋值）
  而且**没有 obj.save()** → 代理编辑被静默丢弃。现在正常保存并记录来源 IP。
* 数据隔离挪到 `AgentScopedAdminMixin`，客户、流水、注单三张表统一生效。
* 删掉了拼错且从未使用的 `DelegateFilter`（`model_admin.model.objcts`）。
* 分页/过滤器/金额渲染统一走 admin_ext。
"""
from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html

from AsianarkAdmin.admin_ext.actions import export_csv
from AsianarkAdmin.admin_ext.badges import cents, choice_badge, dt
from AsianarkAdmin.admin_ext.filters import relative_date_filter
from AsianarkAdmin.admin_ext.pagination import FastPaginationMixin
from AsianarkAdmin.admin_ext.scoping import AgentScopedAdminMixin
from AsianarkAdmin.admin_ext.site import admin_site

from .models import TAgents, TCustomerTrans, TCustomers

CustomerRegFilter = relative_date_filter(
    title="注册时间", parameter_name="reg_range", field_name="create_time"
)
TransTimeFilter = relative_date_filter(
    title="发生时间", parameter_name="date_range", field_name="action_time"
)


@admin.register(TCustomers, site=admin_site)
class TCustomersAdmin(AgentScopedAdminMixin, FastPaginationMixin, admin.ModelAdmin):
    list_display = (
        "loginname",
        "nickname",
        "agentcode",
        "credit_cell",
        "limitid",
        "flag_cell",
        "created_cell",
        "last_login_cell",
        "create_ip",
    )
    list_display_links = ("loginname",)
    search_fields = ("loginname", "nickname", "create_ip")
    search_help_text = "用户名、昵称、注册IP"
    # 老配置 list_filter=('loginname',) → 对全表 DISTINCT 再渲染几万个 option
    list_filter = ("flag", "limitid", "agentcode", CustomerRegFilter)
    list_per_page = 50
    actions = (export_csv,)
    ordering = ("-create_time", "loginname")

    readonly_fields = (
        "loginname",
        "agentcode",
        "create_time",
        "create_ip",
        "last_login_time",
        "last_login_ip",
        "pwd_expired_time",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="信用额度", ordering="credit_cents")
    def credit_cell(self, obj):
        return cents(obj.credit_cents)

    @admin.display(description="状态", ordering="flag")
    def flag_cell(self, obj):
        return choice_badge(obj, "flag")

    @admin.display(description="创建时间", ordering="create_time")
    def created_cell(self, obj):
        return dt(obj.create_time)

    @admin.display(description="最后一次登录", ordering="last_login_time")
    def last_login_cell(self, obj):
        return format_html(
            "{} <span class='quiet'>{}</span>", dt(obj.last_login_time), obj.last_login_ip or ""
        )


@admin.register(TCustomerTrans, site=admin_site)
class TCustomerTransAdmin(AgentScopedAdminMixin, FastPaginationMixin, admin.ModelAdmin):
    list_display = (
        "transid",
        "loginname",
        "agentcode",
        "action",
        "amount_cell",
        "before_cell",
        "after_cell",
        "time_cell",
        "remark",
    )
    list_display_links = ("transid",)
    search_fields = ("transid", "loginname", "action", "remark")
    list_filter = ("action", "agentcode", TransTimeFilter)
    ordering = ("-transid",)
    list_per_page = 50
    actions = (export_csv,)

    readonly_fields = tuple(field.name for field in TCustomerTrans._meta.fields)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="转账额度", ordering="trans_amount_cents")
    def amount_cell(self, obj):
        return cents(obj.trans_amount_cents, signed=True)

    @admin.display(description="操作前额度")
    def before_cell(self, obj):
        return cents(obj.before_credit_cents)

    @admin.display(description="操作后额度")
    def after_cell(self, obj):
        return cents(obj.after_credit_cents)

    @admin.display(description="操作时间", ordering="action_time")
    def time_cell(self, obj):
        return dt(obj.action_time)


@admin.register(TAgents, site=admin_site)
class TAgentsAdmin(FastPaginationMixin, admin.ModelAdmin):
    list_display = ("agentcode", "agentname", "user", "trytype_cell", "flag_cell", "created_cell", "create_ip")
    list_display_links = ("agentcode",)
    search_fields = ("agentcode", "agentname")
    list_filter = ("flag", "trytype")
    ordering = ("agentcode",)
    list_per_page = 50
    autocomplete_fields = ("user",)
    # 系统字段：create_ip 由 save_model 从请求里取，create_time 自动填
    readonly_fields = ("create_time", "create_ip")

    def save_model(self, request, obj, form, change):
        # 老代码：TAgents.create_ip = ip（改的是类的字段描述符）+ 没有 obj.save() → 编辑全部丢失
        obj.create_ip = _client_ip(request)
        obj.save()

    @admin.display(description="是否试用", ordering="trytype")
    def trytype_cell(self, obj):
        return choice_badge(obj, "trytype")

    @admin.display(description="状态", ordering="flag")
    def flag_cell(self, obj):
        return choice_badge(obj, "flag")

    @admin.display(description="创建时间", ordering="create_time")
    def created_cell(self, obj):
        return dt(obj.create_time)


def _client_ip(request) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")
