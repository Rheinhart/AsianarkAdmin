"""后台模板用的标签：保留筛选条件的查询串、数字格式化。"""
from __future__ import annotations

from django import template

register = template.Library()


@register.simple_tag
def qs(cl, remove="", **params):
    """拼查询串：`{% qs cl p=2 %}`、`{% qs cl remove='p,per_page' per_page=100 %}`。

    关键是它包的是 `cl.get_query_string()`，会自动带上当前的搜索词和所有筛选条件，
    切换每页条数 / 翻页时不会把筛选丢掉。
    """
    return cl.get_query_string(params or None, remove.split(",") if remove else None)


@register.filter
def numfmt(value):
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return value


@register.filter
def cents(value):
    """分 → 元（带千分位）。"""
    try:
        return f"{int(value or 0) / 100:,.2f}"
    except (TypeError, ValueError):
        return value
