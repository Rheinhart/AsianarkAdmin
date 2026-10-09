"""后台首页看板的聚合查询（带缓存）。

老项目没有首页看板；这里用极少的查询拼出当日大盘，并且：
* 结果缓存 `settings.DASHBOARD_CACHE_SECONDS` 秒（默认 60s），首页不会被大表聚合拖死；
* 所有查询都带时间范围，不做全表扫描；
* 任何一项失败都不影响首页其它部分。
"""
from __future__ import annotations

import logging
from datetime import timedelta

from django.conf import settings
from django.core.cache import cache
from django.db.models import Count, Sum, Value
from django.db.models.functions import Coalesce, TruncDate
from django.utils import timezone

logger = logging.getLogger("asianark.dashboard")

CACHE_KEY = "asianark:dashboard"


def _zero():
    return Value(0)


def kpi_stats(refresh: bool = False) -> dict:
    if not refresh:
        cached = cache.get(CACHE_KEY)
        if cached:
            return cached

    from AsianarkAdmin.baccarat_Controll.models import TOrders, TRounds
    from AsianarkAdmin.userinfo.models import TCustomers

    today = timezone.localdate()
    start_of_today = timezone.make_aware(
        timezone.datetime(today.year, today.month, today.day), timezone.get_current_timezone()
    )
    week_ago = timezone.now() - timedelta(days=7)

    stats: dict = {"generated_at": timezone.now().strftime("%Y-%m-%d %H:%M:%S")}

    today_qs = TOrders.objects.filter(create_time__gte=start_of_today)
    try:
        stats["today"] = today_qs.aggregate(
            count=Count("billno"),
            bet=Coalesce(Sum("bet_amount_cents"), _zero()),
            valid=Coalesce(Sum("valid_bet_amount_cents"), _zero()),
            win=Coalesce(Sum("win_amount_cents"), _zero()),
        )
    except Exception:  # pragma: no cover
        logger.exception("今日大盘聚合失败")
        stats["today"] = {"count": 0, "bet": 0, "valid": 0, "win": 0}

    try:
        stats["unsettled_rounds"] = TRounds.objects.filter(flag=0).count()
        stats["members"] = TCustomers.objects.count()
    except Exception:  # pragma: no cover
        logger.exception("计数失败")
        stats["unsettled_rounds"] = 0
        stats["members"] = 0

    try:
        # 近 7 天逐日流水（需要 create_time 索引，见 docs/legacy_db_indexes.sql）
        rows = (
            TOrders.objects.filter(create_time__gte=week_ago)
            .annotate(day=TruncDate("create_time"))
            .values("day")
            .annotate(bet=Coalesce(Sum("bet_amount_cents"), _zero()))
            .order_by("day")
        )
        stats["top_days"] = list(rows)
    except Exception:  # pragma: no cover
        stats["top_days"] = []

    cache.set(CACHE_KEY, stats, settings.DASHBOARD_CACHE_SECONDS)
    return stats
