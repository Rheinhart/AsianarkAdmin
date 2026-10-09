# -*- coding: utf-8 -*-
"""模型信号：保存后通知游戏服。

老代码把推送写在 `admin.py` 的模块级 `@receiver` 里，并且在异常分支
`return HttpResponseRedirect("/admin")` —— 信号返回值会被 Django 丢弃，
"通知失败就跳回后台首页"这个意图从来没生效过。现在：
* 信号集中在 signals.py，由 `apps.ready()` 注册（Django 3.2+ 的标准做法，避免重复注册）；
* 失败只记日志 + 进重试队列（`services.flush_retries()` / `manage.py flush_push_queue`）；
* 不在信号里做跳转、不返回值。
"""
from __future__ import annotations

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from . import services
from .models import TPersonalLimitset, TTableLimitset, TBulletin


def _skip_raw(**kwargs) -> bool:
    """loaddata / 数据迁移时不推送。"""
    return bool(kwargs.get("raw"))


@receiver(post_save, sender=TBulletin, dispatch_uid="bulletin_push")
def push_bulletin(sender, instance, created, **kwargs):
    if _skip_raw(**kwargs):
        return
    services.push_bulletin(instance)


@receiver(post_save, sender=TTableLimitset, dispatch_uid="table_limit_push")
def push_table_limit(sender, instance, created, **kwargs):
    if _skip_raw(**kwargs):
        return
    services.push_table_limit(instance)


@receiver(post_save, sender=TPersonalLimitset, dispatch_uid="personal_limit_push")
def push_personal_limit(sender, instance, created, **kwargs):
    if _skip_raw(**kwargs):
        return
    services.push_personal_limit(instance)
