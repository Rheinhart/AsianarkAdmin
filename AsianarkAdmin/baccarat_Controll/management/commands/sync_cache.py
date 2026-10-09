# -*- coding: utf-8 -*-
"""手动同步 t_video / t_table 的 memcache 内存模型。

老代码是在 `changelist_view` 里做的 —— 每打开一次列表页就同步一次，
还顺手写一条 LogEntry。现在改成显式操作（列表页也有对应 action）。
"""
from django.core.management.base import BaseCommand

from AsianarkAdmin.baccarat_Controll import services


class Command(BaseCommand):
    help = "同步视频/桌台的 memcache 内存模型（需要 ASIANARK_MEMCACHE_ENABLED=1）"

    def handle(self, *args, **options):
        if not services.memcache_enabled():
            self.stdout.write(self.style.WARNING("memcache 未启用（ASIANARK_MEMCACHE_ENABLED=0），跳过。"))
            return
        if services.sync_all():
            self.stdout.write(self.style.SUCCESS("同步完成。"))
        else:
            self.stdout.write(self.style.ERROR("同步失败，详见日志。"))
