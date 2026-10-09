"""列表页顶部统计条：合计跟随当前筛选，小计只算当前页。

老实现（`TOrdersAdmin.changelist_view`）每次打开/翻页会：
* 对**未筛选**的 t_orders 做 5 次全表取数（在 Python 里 sum）+ 3 次 COUNT；
* 把"未筛选全表的前 N 行"标成"本页小计" —— 既不是当前页也不是当前筛选，数字不可信；
* `float(win) / valid_bet_amount_total` 在空表时 ZeroDivisionError。

这里改成：一次 `cl.queryset.aggregate()`（跟随搜索+筛选）+ 当前页内存求和 + 防除零，
结果集过大时只统计前 `stats_probe` 行并明确标出"部分合计"。
"""
from __future__ import annotations

import logging

from django.db.models import Sum

logger = logging.getLogger("asianark.stats")

FORMATTERS = {
    "int": lambda v: f"{int(v or 0):,}",
    "cents": lambda v: f"{int(v or 0) / 100:,.2f}",
    "cents_signed": lambda v: f"{int(v or 0) / 100:+,.2f}",
    "pct": lambda v: f"{float(v or 0):.2f}%",
}


class ChangelistStatsMixin:
    """在 changelist 顶部注入 `stats`（合计）与 `page_stats`（本页小计）。

    子类声明::

        stats_specs = [
            {"key": "bet", "label": "投注额", "expr": Sum("bet_amount_cents"), "fmt": "cents"},
        ]
        stats_ratio = {"key": "rate", "label": "盈利率", "num": "win", "den": "valid", "scale": 100}
        page_specs = [{"key": "bet", "label": "投注额", "field": "bet_amount_cents", "fmt": "cents"}]
    """

    stats_specs: list[dict] = []
    stats_ratio: dict | None = None
    page_specs: list[dict] = []
    stats_probe = 50_000          # 超过这个行数只做部分合计，避免全表扫描

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        cl = getattr(response, "context_data", {}).get("cl")
        if cl is None or not self.stats_specs:
            return response
        try:
            response.context_data["stats"] = self.build_stats(request, cl)
        except Exception:  # 统计条出错不应该让整个列表页 500
            logger.exception("列表统计计算失败")
            response.context_data["stats"] = None
        return response

    def build_stats(self, request, cl) -> dict:
        paginator = getattr(cl, "paginator", None)
        total = cl.result_count
        partial = bool(getattr(paginator, "estimated", False)) or total > self.stats_probe
        queryset = cl.queryset[: self.stats_probe] if partial else cl.queryset

        agg = queryset.aggregate(**{spec["key"]: spec["expr"] for spec in self.stats_specs})

        items = []
        for spec in self.stats_specs:
            value = agg.get(spec["key"]) or 0
            items.append(self._stat_item(spec, value))

        if self.stats_ratio:
            ratio_spec = self.stats_ratio
            denominator = agg.get(ratio_spec["den"]) or 0
            numerator = agg.get(ratio_spec["num"]) or 0
            ratio = (numerator * ratio_spec.get("scale", 1)) / denominator if denominator else 0
            items.append(self._stat_item(ratio_spec, ratio))

        page_items = []
        if self.page_specs:
            rows = list(cl.result_list)
            for spec in self.page_specs:
                field = spec.get("field")
                total_on_page = sum(int(getattr(row, field, 0) or 0) for row in rows)
                page_items.append(self._stat_item(spec, total_on_page))

        return {
            "items": items,
            "page_items": page_items,
            "count": total,
            "count_partial": partial,
            "page_rows": len(list(cl.result_list)),
            "limit": self.stats_probe,
        }

    @staticmethod
    def _stat_item(spec, value) -> dict:
        fmt = FORMATTERS.get(spec.get("fmt", "int"), FORMATTERS["int"])
        return {
            "key": spec["key"],
            "label": spec["label"],
            "value": value,
            "text": fmt(value),
            "kind": spec.get("kind", ""),
        }


# 常用聚合，给各 Admin 拼 stats_specs 用
sum_cents = Sum
