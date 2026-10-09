# -*- coding: utf-8 -*-
"""后台操作日志（LogEntry）。

老代码在 `TVideo/TTable.changelist_view` 里每次 GET 都 `log_change(...)` 写一条
"自动同步所有视频缓存数据库" —— 审计日志被刷成噪音，而且列表页变慢。
现在只在真正的操作（保存、删除、批量动作）里记日志。
"""
from __future__ import annotations

from django.contrib import admin
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry

from AsianarkAdmin.admin_ext.badges import dt
from AsianarkAdmin.admin_ext.filters import relative_date_filter
from AsianarkAdmin.admin_ext.pagination import FastPaginationMixin
from AsianarkAdmin.admin_ext.site import admin_site

LogTimeFilter = relative_date_filter(
    title="操作时间", parameter_name="date_range", field_name="action_time"
)

ACTION_NAMES = {
    ADDITION: "新增",
    CHANGE: "修改",
    DELETION: "删除",
}


@admin.register(LogEntry, site=admin_site)
class LogEntryAdmin(FastPaginationMixin, admin.ModelAdmin):
    list_display = ("id", "time_cell", "user", "action_name", "content_type", "object_repr", "change_message")
    list_display_links = ("id",)
    search_fields = ("object_repr", "change_message", "user__username")
    list_filter = ("action_flag", LogTimeFilter)
    ordering = ("-id",)
    list_per_page = 50

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    @admin.display(description="操作时间", ordering="action_time")
    def time_cell(self, obj):
        return dt(obj.action_time)

    @admin.display(description="动作", ordering="action_flag")
    def action_name(self, obj):
        return ACTION_NAMES.get(obj.action_flag, str(obj.action_flag))
