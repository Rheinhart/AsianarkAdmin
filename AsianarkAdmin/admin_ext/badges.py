"""列表页小部件：金额（分）、状态徽标、时间。

老代码里每个 ModelAdmin 都手写一遍：

    def mycreate_time(self, obj):
        if not obj.create_time: return obj.create_time
        return obj.create_time.strftime('%Y-%m-%d %H:%M:%S')

十几份重复，而且绕过了 Django 的时区格式化（老 settings 是 UTC，显示直接差 8 小时）。
这里统一：时间用 `localtime` + settings.DATETIME_FORMAT，金额把"分"转成带千分位的元。
"""
from __future__ import annotations

from django.utils.formats import date_format
from django.utils.html import format_html, mark_safe
from django.utils import timezone

OK, WARN, BAD, MUTED, VIP = "ok", "warn", "bad", "muted", "vip"


def badge(text, kind: str = MUTED):
    return format_html('<span class="cbadge cbadge-{}">{}</span>', kind, text)


def dt(value):
    """安全的时间列渲染：None 显示为 —，其余按 settings.DATETIME_FORMAT（本地时区）。"""
    if not value:
        return mark_safe('<span class="quiet">—</span>')
    if timezone.is_aware(value):
        value = timezone.localtime(value)
    return format_html('<span class="mono">{}</span>', date_format(value, "DATETIME_FORMAT"))


def cents(value, *, signed: bool = False, kind: str | None = None):
    """把"分"渲染成带千分位的金额，并按正负着色。"""
    try:
        cents_value = int(value or 0)
    except (TypeError, ValueError):
        return badge("—", MUTED)
    if kind is None:
        kind = OK if cents_value > 0 else BAD if cents_value < 0 else MUTED
    yuan = cents_value / 100
    text = f"{yuan:+,.2f}" if signed else f"{yuan:,.2f}"
    return format_html('<span class="money money-{}">{}</span>', kind, text)


def number(value):
    try:
        return format_html('<span class="mono">{:,}</span>', int(value or 0))
    except (TypeError, ValueError):
        return badge("—", MUTED)


def choice_badge(obj, field: str = "flag", kind_map: dict | None = None):
    """把带 choices 的状态字段渲染成徽标。"""
    value = getattr(obj, field)
    text = getattr(obj, f"get_{field}_display", lambda: value)()
    kinds = {0: OK, 1: BAD, 8: VIP, -1: MUTED}
    return badge(text, (kind_map or kinds).get(value, MUTED))
