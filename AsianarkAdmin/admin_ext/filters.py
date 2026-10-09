"""列表页过滤器。

老配置里 `list_filter` 基本是"把所有字段都列上"，例如注单页
`list_filter = ('loginname','create_time','reckon_time','flag')`：
`loginname` 这种高基数字段会让 admin 对全表做一次 `SELECT DISTINCT`，
再渲染几万个 `<option>`，每翻一页都付一次这个钱。

规则：
* 有 choices 的字段（flag / gametype / playtype）→ 直接用字符串 filter，不查库；
* 时间字段 → 用这里的 `RelativeDateFilter`（今天/近7天…），需要精确区间时保留
  Django 对 DateTimeField 自带的"开始/结束"输入（它不查 DISTINCT，是廉价的）；
* 高基数字段（loginname / videoid / url / tableid / seats）→ 不进 list_filter，走搜索框。
"""
from __future__ import annotations

from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

DEFAULT_LOOKUPS = [
    ("1d", "今天", timedelta(days=1)),
    ("3d", "近 3 天", timedelta(days=3)),
    ("7d", "近 7 天", timedelta(days=7)),
    ("30d", "近 30 天", timedelta(days=30)),
    ("90d", "近 90 天", timedelta(days=90)),
    ("365d", "近一年", timedelta(days=365)),
]


class RelativeDateFilter(admin.SimpleListFilter):
    """按相对时间范围过滤。

    不用 admin 自带的 `date_hierarchy`：它会对整张表做 DISTINCT(截断日期)，
    几十万行的 t_orders 上比这里一条 `WHERE create_time >= ?` 贵两个数量级。
    """

    title = "时间范围"
    parameter_name = "date_range"
    field_name = "create_time"
    lookups_spec = DEFAULT_LOOKUPS

    def lookups(self, request, model_admin):
        return [(key, label) for key, label, _ in self.lookups_spec]

    def queryset(self, request, queryset):
        for key, _label, delta in self.lookups_spec:
            if self.value() == key:
                return queryset.filter(**{f"{self.field_name}__gte": timezone.now() - delta})
        return queryset


def relative_date_filter(
    *, title: str, parameter_name: str, field_name: str, lookups: list | None = None
) -> type[RelativeDateFilter]:
    """生成一个绑定了具体字段的过滤器类，避免每个 Admin 复制一份。"""
    return type(
        f"Range_{parameter_name}",
        (RelativeDateFilter,),
        {
            "title": title,
            "parameter_name": parameter_name,
            "field_name": field_name,
            "lookups_spec": lookups or DEFAULT_LOOKUPS,
        },
    )


class ChoicesFromFilter(admin.SimpleListFilter):
    """给"没有 choices 但取值有限"的字段做下拉过滤（如代理 agentcode）。"""

    title = ""
    parameter_name = ""
    field_name = ""

    def choices(self, request, model_admin) -> list[tuple[str, str]]:  # pragma: no cover - 接口
        return []

    def lookups(self, request, model_admin):
        return self.choices(request, model_admin)

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset
        return queryset.filter(**{self.field_name: value})
