# -*- coding: utf-8 -*-
"""测试辅助：业务表是 managed=False，测试库不会自动建，这里手动建一次。"""
from __future__ import annotations

from django.db import connection

from AsianarkAdmin.tables import business_models


def ensure_business_tables() -> None:
    existing = set(connection.introspection.table_names())
    with connection.schema_editor() as editor:
        for model in business_models():
            if model._meta.db_table not in existing:
                editor.create_model(model)


class BusinessTablesTestCaseMixin:
    """在 TestCase 里混入：建表发生在 TestCase 的事务之外，测试结束不会残留脏结构。"""

    @classmethod
    def setUpClass(cls):
        ensure_business_tables()
        super().setUpClass()
