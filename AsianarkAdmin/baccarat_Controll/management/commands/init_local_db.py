# -*- coding: utf-8 -*-
"""在本地开发库（sqlite）里创建业务表。

线上老库的表由游戏服维护，模型全部 managed=False，所以 `migrate` 不会建这些表。
本地开发跑：

    python manage.py migrate            # Django 自己的表
    python manage.py init_local_db      # t_video / t_orders / ... 业务表
    python manage.py seed_demo --reset  # 演示数据
"""
from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import connection, connections

from AsianarkAdmin.tables import business_models


class Command(BaseCommand):
    help = "在本地开发库中创建业务表（线上老库不要跑）"

    def add_arguments(self, parser):
        parser.add_argument("--drop", action="store_true", help="先删除已存在的业务表")
        parser.add_argument("--force", action="store_true", help="允许在非 sqlite 上执行")

    def handle(self, *args, **options):
        conn = connections["default"]
        if conn.vendor != "sqlite" and not options["force"]:
            self.stdout.write(self.style.WARNING(
                f"当前数据库是 {conn.vendor}。业务表由老库维护，确认要执行请加 --force。"
            ))
            return

        models = business_models()
        existing = set(connection.introspection.table_names())

        with connection.schema_editor() as editor:
            if options["drop"]:
                for model in reversed(models):
                    if model._meta.db_table in existing:
                        editor.delete_model(model)
                self.stdout.write("已删除旧表。")
                existing = set(connection.introspection.table_names())

            created = []
            for model in models:
                if model._meta.db_table in existing:
                    continue
                editor.create_model(model)
                created.append(model._meta.db_table)

        if created:
            self.stdout.write(self.style.SUCCESS(f"已创建 {len(created)} 张表：{', '.join(created)}"))
        else:
            self.stdout.write("所有业务表都已存在，无需创建。")
