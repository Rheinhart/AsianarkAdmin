#coding:utf8
"""
@__author__ = 'Thomas'
"""
from django.contrib import admin

from django.contrib.admin.models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):

    def myaction_time(self,obj):
        if not obj.action_time:
            return obj.action_time
        else:
            return obj.action_time.strftime('%Y-%m-%d %H:%M:%S')
    myaction_time.short_description = u'开始时间'
    myaction_time.admin_order_field = 'action_time'

    list_display = ('id','myaction_time','user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message')





