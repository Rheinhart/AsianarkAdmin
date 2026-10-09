# -*- coding: utf-8 -*-
"""与游戏服 / memcache 的集成层。

老代码的问题：
* 推送代码散在每个 ModelAdmin 和信号里，`requests.get(url, data)` **没有 timeout**，
  游戏服挂了后台就卡死；`data` 有时传 list，requests 会去 urlencode 一个字符串列表而报错；
* 信号里 `return HttpResponseRedirect("/admin")` —— 信号返回值会被丢弃，"通知失败就跳转"从未生效；
* `from memopr import memopr` 在**导入模型时**就连接 MySQL + memcached，任何 manage.py 命令都有外部依赖。

这里统一成一个可关闭、可超时、失败会记录并重试的入口。
"""
from __future__ import annotations

import logging
from functools import wraps

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger("asianark.services")

QUEUE_KEY = "asianark:push:retry_queue"
QUEUE_MAX = 200


class PushError(Exception):
    """游戏服返回了非预期应答。"""


# --------------------------------------------------------------------- 游戏服 HTTP 推送
def expected_answer(command: int) -> str:
    """游戏服的应答约定：60000 + (command - 50000)，即 command + 10000。"""
    return str(command + 10000)


def push(endpoint: str, command: int, params: dict | None = None, *, queue_on_fail: bool = True) -> bool:
    """向游戏服发一条指令。返回是否成功；失败只记录日志，不抛给调用方。"""
    cfg = settings.GAME_SERVER["default"]
    if not cfg.get("ENABLED", True):
        logger.info("推送已禁用（ASIANARK_PUSH_ENABLED=0），跳过 command=%s", command)
        return False

    url = f"http://{cfg['URL']}:{cfg['PORT']}/{endpoint}"
    payload = {"command": command}
    payload.update(params or {})

    try:
        response = requests.get(url, params=payload, timeout=cfg.get("TIMEOUT", 3))
    except Exception as exc:  # requests.RequestException 以及任何意外（坏 payload 等）
        logger.warning("游戏服推送失败 %s command=%s: %s", url, command, exc)
        if queue_on_fail:
            enqueue_retry({"endpoint": endpoint, "command": command, "params": payload})
        return False

    body = (response.text or "").strip()
    want = expected_answer(command)
    if body != want:
        logger.warning("游戏服应答异常 %s command=%s: 期望 %s，收到 %r", url, command, want, body[:200])
        if queue_on_fail:
            enqueue_retry({"endpoint": endpoint, "command": command, "params": payload})
        return False
    logger.info("游戏服推送成功 command=%s", command)
    return True


def enqueue_retry(item: dict) -> None:
    queue = cache.get(QUEUE_KEY, [])
    queue.append(item)
    cache.set(QUEUE_KEY, queue[-QUEUE_MAX:], 60 * 60 * 24)


def pending_retries() -> list[dict]:
    return cache.get(QUEUE_KEY, [])


def flush_retries(limit: int = 50) -> tuple[int, int]:
    """重放失败队列，返回 (成功数, 仍失败数)。"""
    queue = pending_retries()
    if not queue:
        return 0, 0
    remaining, ok = [], 0
    for item in queue:
        if push(item["endpoint"], item["command"], item.get("params"), queue_on_fail=False):
            ok += 1
        else:
            remaining.append(item)
    if remaining:
        cache.set(QUEUE_KEY, remaining[-QUEUE_MAX:], 60 * 60 * 24)
    else:
        cache.delete(QUEUE_KEY)
    return ok, len(remaining)


# --------------------------------------------------------------------- 各业务对象的推送封装


def _guarded(fn):
    """推送封装层自己出错也不应该冒到后台视图里：保存已经成功，推送失败只记日志。"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:  # pragma: no cover - 防御性兜底
            logger.exception("推送封装异常：%s", fn.__name__)
            return False

    return wrapper


@_guarded
def push_video(obj, created: bool) -> bool:
    return push(
        "video",
        50003 if created else 50004,
        {
            "videoid": obj.videoid,
            "url": obj.url,
            "flag": obj.flag,
            "bettime": obj.bettime,
            "gametype": obj.gametype,
        },
    )


@_guarded
def push_videos_deleted(videoids: list[str]) -> bool:
    # 老代码把 list 直接塞给 requests.data；这里显式拼成逗号串，避免 urlencode 报错
    return push("video", 50005, {"videoids": ",".join(videoids)})


@_guarded
def push_table(obj, created: bool) -> bool:
    return push(
        "table",
        50006 if created else 50007,
        {
            "videoid": obj.videoid_id if hasattr(obj, "videoid_id") else obj.videoid,
            "gametype": obj.gametype,
            "tableid": obj.tableid,
            "flag": obj.flag,
            "seats": obj.seats,
            "limitid": obj.limitid,
        },
    )


@_guarded
def push_table_limit(obj) -> bool:
    return push(
        "tablelimit",
        50009,
        {
            # 注意：游服协议里的 key 就是 playtaye（历史拼写）。要改成 playtype 必须同步改游服。
            "playtaye": obj.playtype,
            "minval_cents": obj.min_cents,
            "maxval_cents": obj.max_cents,
            "limitid": obj.limitid,
            "flag": obj.flag,
        },
    )


@_guarded
def push_personal_limit(obj) -> bool:
    return push(
        "personallimit",
        50011,
        {
            "playtaye": obj.playtype,
            "minval_cents": obj.min_cents,
            "maxval_cents": obj.max_cents,
            "limitid": obj.limitid,
            "flag": obj.flag,
        },
    )


@_guarded
def push_bulletin(obj) -> bool:
    # 保持老协议：只发 command，游服自己重新拉公告列表
    return push("bulletin", 50013)


@_guarded
def recalc_round(roundcode: str, cards: str = "") -> bool:
    return push("round", 50016, {"roundcode": roundcode, "cards": cards or ""})


@_guarded
def cancel_round(roundcode: str) -> bool:
    return push("round", 50017, {"roundcode": roundcode})


@_guarded
def notify_login(user) -> bool:
    return push("controller", 50001, {"controller": getattr(user, "username", str(user))})


# --------------------------------------------------------------------- firefly memcache（t_video / t_table）
_memopr = None


def memopr():
    """懒加载：只有真正需要时才连接 memcache / 老库。"""
    global _memopr
    if _memopr is None:
        from AsianarkAdmin.baccarat_Controll.memopr import get_memopr

        _memopr = get_memopr()
    return _memopr


def memcache_enabled() -> bool:
    return bool(settings.MEMCACHE.get("ENABLED"))


def _safe(fn_name, *args) -> bool:
    if not memcache_enabled():
        return False
    try:
        getattr(memopr(), fn_name)(*args)
        return True
    except Exception as exc:  # 缓存同步失败不应该让后台保存失败
        logger.warning("memcache 同步失败 %s: %s", fn_name, exc)
        return False


def sync_video(obj) -> bool:
    return _safe("changeVideoInMem", _video_payload(obj))


def sync_table(obj) -> bool:
    return _safe("changeTableInMem", _table_payload(obj))


def sync_all() -> bool:
    ok = _safe("syncVideoMemAndDb")
    return _safe("syncTableMemAndDb") and ok


def _video_payload(obj) -> dict:
    return {
        "videoid": obj.videoid,
        "url": obj.url,
        "flag": obj.flag,
        "bettime": obj.bettime,
        "gametype": obj.gametype,
    }


def _table_payload(obj) -> dict:
    return {
        "videoid": obj.videoid_id if hasattr(obj, "videoid_id") else obj.videoid,
        "gametype": obj.gametype,
        "tableid": obj.tableid,
        "flag": obj.flag,
        "seats": obj.seats,
        "limitid": obj.limitid,
    }
