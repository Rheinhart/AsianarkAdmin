# -*- coding: utf-8 -*-
"""重放推送失败队列（游戏服恢复后手动/定时执行）。"""
from django.core.management.base import BaseCommand

from AsianarkAdmin.baccarat_Controll import services


class Command(BaseCommand):
    help = "重放发往游戏服但失败了的指令"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=200)

    def handle(self, *args, **options):
        pending = services.pending_retries()
        if not pending:
            self.stdout.write("队列为空。")
            return
        self.stdout.write(f"待重放 {len(pending)} 条…")
        ok, failed = services.flush_retries(limit=options["limit"])
        if failed:
            self.stdout.write(self.style.WARNING(f"成功 {ok}，仍失败 {failed}（已留在队列）"))
        else:
            self.stdout.write(self.style.SUCCESS(f"全部重放成功：{ok} 条"))
