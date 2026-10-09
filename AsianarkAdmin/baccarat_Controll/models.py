# -*- coding: utf-8 -*-
"""游戏业务模型（对应老库 bjl 的 t_* 表）。

改动要点
--------
* Python 3 / `__str__`；时间默认值一律用 `timezone.now`（可调用），
  老代码里 `default=datetime.datetime.now().strftime(...)` 和类属性 `tomorrow`
  都是**导入时求值一次**的固定值，公告的创建/到期时间会卡在进程启动那一刻。
* 所有表 `managed=False`（表结构属于老库，Django 不碰）。本地开发用
  `python manage.py init_local_db` 在 sqlite 里建同样的表（见该命令）。
* 模型不再在导入时连 memcache（老代码 `from memopr import memopr` 会触发模块级连接）。
  缓存/游戏服同步挪到 `services.py`，由 admin 与信号显式调用。
* `Meta.indexes` 只在 managed=True 时生效；线上老库的索引脚本见 docs/legacy_db_indexes.sql。
"""
from __future__ import annotations

from datetime import timedelta

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from AsianarkAdmin.tools.choicecode import FLAG, GAMETYPE, LIMITID, ORDERFLAG, PAIR, TRYTYPE


def _default_expired_time():
    return timezone.now() + timedelta(days=1)


class DjangoMigrations(models.Model):
    """老库的 django_migrations 只读视图（不参与建表）。"""

    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"
        verbose_name = "迁移记录"
        verbose_name_plural = "迁移记录"

    def __str__(self):
        return f"{self.app}: {self.name}"


class TBulletin(models.Model):
    """公告信息。"""

    bulletinid = models.AutoField(verbose_name="公告ID", primary_key=True)
    create_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)
    expired_time = models.DateTimeField(verbose_name="到期时间", default=_default_expired_time)
    text = models.TextField(max_length=200, verbose_name="公告内容")
    flag = models.IntegerField(verbose_name="是否禁用", choices=FLAG, default=0)  # 0:启用 1:禁用

    class Meta:
        managed = False
        db_table = "t_bulletin"
        verbose_name = "公告信息"
        verbose_name_plural = "公告信息"
        ordering = ("-bulletinid",)

    def __str__(self):
        return f"公告 {self.bulletinid}"


class TVideo(models.Model):
    """视频流。"""

    videoid = models.CharField(
        verbose_name="视频ID",
        primary_key=True,
        max_length=16,
        help_text="删除视频前请先删除引用它的桌台",
    )
    gametype = models.CharField(verbose_name="游戏类型", max_length=16, choices=GAMETYPE, default="BJL")
    flag = models.IntegerField(db_column="Flag", verbose_name="是否禁用", choices=FLAG, default=0)
    bettime = models.IntegerField(db_column="BetTime", verbose_name="下注倒计时(秒)", default=0)
    url = models.CharField(db_column="URL", max_length=160, verbose_name="URL")

    class Meta:
        managed = False
        db_table = "t_video"
        verbose_name = "视频信息"
        verbose_name_plural = "视频信息"
        ordering = ("videoid",)

    def __str__(self):
        return self.videoid


class TTableLimitset(models.Model):
    """桌台限红。"""

    id = models.AutoField(primary_key=True)
    limitid = models.CharField(db_column="LimitID", verbose_name="限红ID", max_length=4)
    playtype = models.IntegerField(
        db_column="PlayType", verbose_name="玩法", validators=[MinValueValidator(0), MaxValueValidator(9999)]
    )
    min_cents = models.IntegerField(db_column="Min_Cents", verbose_name="最小下注额度", default=0)
    max_cents = models.IntegerField(db_column="Max_Cents", verbose_name="最大下注额度", default=100)
    flag = models.IntegerField(db_column="Flag", verbose_name="是否禁用", choices=FLAG, default=0)

    class Meta:
        managed = False
        db_table = "t_table_limitset"
        verbose_name = "桌台限红表"
        verbose_name_plural = "桌台限红表"
        ordering = ("limitid", "playtype")
        indexes = [models.Index(fields=["limitid", "playtype"], name="t_table_limit_idx")]

    def __str__(self):
        return f"桌台限红 {self.limitid},{self.playtype}"


class TTable(models.Model):
    """桌台。"""

    tableid = models.CharField(db_column="TableID", verbose_name="桌台ID", primary_key=True, max_length=16)
    videoid = models.ForeignKey(
        TVideo,
        db_column="VideoID",
        on_delete=models.PROTECT,
        verbose_name="视频ID",
        help_text="不要在这里删除视频",
    )
    gametype = models.CharField(
        db_column="GameType", verbose_name="游戏类型", choices=GAMETYPE, default="BJL", max_length=16
    )
    limitid = models.CharField(
        db_column="LimitID",
        choices=LIMITID,
        verbose_name="限红ID",
        help_text="请与桌台限红表中数据保持一致",
        max_length=4,
    )
    seats = models.IntegerField(
        db_column="Seats",
        verbose_name="座位数",
        default=7,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
    )
    flag = models.IntegerField(db_column="Flag", verbose_name="是否禁用", choices=FLAG, default=0)

    class Meta:
        managed = False
        db_table = "t_table"
        verbose_name = "桌台信息"
        verbose_name_plural = "桌台信息"
        ordering = ("tableid",)

    def __str__(self):
        return self.tableid


class TPersonalLimitset(models.Model):
    """个人限红。"""

    id = models.AutoField(primary_key=True)
    limitid = models.CharField(db_column="LimitID", verbose_name="限红ID", max_length=11)
    playtype = models.IntegerField(
        db_column="PlayType", verbose_name="玩法", validators=[MinValueValidator(0), MaxValueValidator(9999)]
    )
    min_cents = models.IntegerField(db_column="Min_Cents", verbose_name="最小下注额度", default=0)
    max_cents = models.IntegerField(db_column="Max_Cents", verbose_name="最大下注额度", default=100)
    flag = models.IntegerField(db_column="Flag", verbose_name="是否禁用", choices=FLAG, default=0)

    class Meta:
        managed = False
        db_table = "t_personal_limitset"
        verbose_name = "个人限红表"
        verbose_name_plural = "个人限红表"
        ordering = ("limitid", "playtype")

    def __str__(self):
        return f"个人限红 {self.limitid},{self.playtype}"


class TOrders(models.Model):
    """游戏注单（大表：分页/统计都要按这个表设计）。"""

    billno = models.IntegerField(primary_key=True, verbose_name="注单号码")
    gametype = models.CharField(max_length=16, verbose_name="游戏类型", choices=GAMETYPE)
    loginname = models.CharField(max_length=32, verbose_name="账户名称", db_index=True)
    agentcode = models.IntegerField(db_column="AgentCode", verbose_name="代理CODE", db_index=True)
    roundcode = models.CharField(max_length=16, verbose_name="游戏局号")
    videoid = models.CharField(db_column="videoid", max_length=16, verbose_name="视频ID", default="")
    tableid = models.CharField(db_column="tableid", max_length=16, verbose_name="桌台ID", default="")
    seat = models.IntegerField(verbose_name="位置", validators=[MinValueValidator(0), MaxValueValidator(9999)])
    dealer = models.CharField(max_length=16, verbose_name="荷官")
    flag = models.IntegerField(db_column="Flag", verbose_name="结算标志", choices=ORDERFLAG, default=0)
    playtype = models.IntegerField(verbose_name="玩法", validators=[MinValueValidator(0), MaxValueValidator(9999)])
    bet_amount_cents = models.IntegerField(default=0, verbose_name="投注额")
    valid_bet_amount_cents = models.IntegerField(default=0, verbose_name="有效投注额")
    win_amount_cents = models.IntegerField(default=0, verbose_name="盈利额")
    hashcode = models.CharField(max_length=32, verbose_name="哈希值")
    before_credit_cents = models.IntegerField(
        db_column="Before_credit_Cents", verbose_name="原额度", default=0
    )
    after_credit_cents = models.IntegerField(db_column="After_credit_Cents", verbose_name="现额度", default=0)
    create_time = models.DateTimeField(
        db_column="Create_time", verbose_name="创建时间", default=timezone.now, db_index=True
    )
    reckon_time = models.DateTimeField(db_column="Reckon_time", verbose_name="结算时间", blank=True, null=True)
    create_ip = models.GenericIPAddressField(verbose_name="创建IP", max_length=39)

    class Meta:
        managed = False
        db_table = "t_orders"
        verbose_name = "游戏注单"
        verbose_name_plural = "游戏注单"
        # 稳定排序：翻页不重不漏；按主键兜底避免同一秒内乱序
        ordering = ("-create_time", "-billno")
        indexes = [
            models.Index(fields=["-create_time", "-billno"], name="t_orders_time_bill_idx"),
            models.Index(fields=["loginname", "-create_time"], name="t_orders_user_time_idx"),
            models.Index(fields=["roundcode"], name="t_orders_round_idx"),
        ]

    def __str__(self):
        return f"{self.billno}"


class TRounds(models.Model):
    """游戏局记录。"""

    roundcode = models.CharField(primary_key=True, max_length=16, verbose_name="游戏局号")
    gametype = models.CharField(max_length=4, verbose_name="游戏类型", choices=GAMETYPE)
    videoid = models.CharField(max_length=16, verbose_name="视频ID")
    dealer = models.CharField(max_length=16, verbose_name="荷官", blank=True, null=True)
    flag = models.IntegerField(db_column="Flag", verbose_name="结算标志", choices=FLAG, default=0)
    cards = models.CharField(
        max_length=24, blank=True, null=True, verbose_name="牌值列表", help_text="请按 1,2,3:4,5,6 格式输入"
    )
    cardnum = models.IntegerField(
        blank=True, null=True, verbose_name="牌张数", validators=[MinValueValidator(0), MaxValueValidator(9999)]
    )
    pair = models.IntegerField(blank=True, null=True, choices=PAIR, verbose_name="庄闲对")
    bankerpoint = models.IntegerField(
        blank=True, null=True, verbose_name="庄家点数", validators=[MinValueValidator(0), MaxValueValidator(9999)]
    )
    playerpoint = models.IntegerField(
        blank=True, null=True, verbose_name="闲家点数", validators=[MinValueValidator(0), MaxValueValidator(9999)]
    )
    begintime = models.DateTimeField(verbose_name="开始时间", default=timezone.now, db_index=True)
    closetime = models.DateTimeField(blank=True, null=True, verbose_name="结束时间")
    shoecode = models.CharField(max_length=16, verbose_name="靴号")

    class Meta:
        managed = False
        db_table = "t_rounds"
        verbose_name = "游戏局记录"
        verbose_name_plural = "游戏局记录"
        ordering = ("-roundcode",)
        indexes = [
            models.Index(fields=["-begintime"], name="t_rounds_begin_idx"),
            models.Index(fields=["flag"], name="t_rounds_flag_idx"),
        ]

    def __str__(self):
        return self.roundcode


class TRecalcRounds(models.Model):
    """重新结算游戏局的操作记录。"""

    actionid = models.IntegerField(primary_key=True, verbose_name="操作ID")
    create_time = models.DateTimeField(
        db_column="Create_time", verbose_name="创建时间", default=timezone.now, db_index=True
    )
    action = models.CharField(max_length=64, verbose_name="操作")
    roundcode = models.CharField(max_length=16, verbose_name="游戏局号")

    class Meta:
        managed = False
        db_table = "t_recalc_rounds"
        verbose_name = "重新结算游戏局记录"
        verbose_name_plural = "重新结算游戏局记录"
        ordering = ("-actionid",)

    def __str__(self):
        return f"{self.actionid} {self.action} {self.roundcode}"
