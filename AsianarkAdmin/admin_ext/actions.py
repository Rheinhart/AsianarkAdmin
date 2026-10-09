"""可复用的 admin actions。

注意：老代码把"每页显示 N 条"也做成 action（45 个方法），那是机制误用 ——
action 的契约是"对勾选的记录做批量写操作"。这里只放真正的批量操作。
"""
from __future__ import annotations

import csv

from django.http import HttpResponse


def export_csv(modeladmin, request, queryset):
    """导出所选行为 CSV（只导具体字段，不导计算字段）。"""
    opts = modeladmin.model._meta
    fields = [f for f in opts.concrete_fields if not getattr(f, "remote_field", None)]

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{opts.model_name}.csv"'
    writer = csv.writer(response)
    writer.writerow([f.verbose_name for f in fields])
    for obj in queryset.iterator(chunk_size=500):
        writer.writerow([getattr(obj, f.attname) for f in fields])
    return response


export_csv.short_description = "📤 导出为 CSV"
export_csv.allowed_permissions = ("view",)
