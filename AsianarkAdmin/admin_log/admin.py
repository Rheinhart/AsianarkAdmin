#coding:utf8
"""
@__author__ = 'Thomas'
"""
from django.contrib import admin
from django.contrib.admin.models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """管理员操作日志
    """

    def myaction_time(self,obj):
        if not obj.action_time:
            return obj.action_time
        else:
            return obj.action_time.strftime('%Y-%m-%d %H:%M:%S')
    myaction_time.short_description = u'开始时间'
    myaction_time.admin_order_field = 'action_time'

    list_display = ('id','myaction_time','user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message')
    ordering = ('-id',)

    def setListPerPage_30(self,request,queryset):
        admin.ModelAdmin.list_per_page=30
    setListPerPage_30.short_description = u'每页显示30条'
    def setListPerPage_50(self,request,queryset):
        admin.ModelAdmin.list_per_page=50
    setListPerPage_50.short_description = u'每页显示50条'
    def setListPerPage_100(self,request,queryset):
        admin.ModelAdmin.list_per_page=100
    setListPerPage_100.short_description = u'每页显示100条'
    def setListPerPage_300(self,request,queryset):
        admin.ModelAdmin.list_per_page=300
    setListPerPage_300.short_description = u'每页显示300条'
    def setListPerPage_1000(self,request,queset):
        admin.ModelAdmin.list_per_page=1000
    setListPerPage_1000.short_description = u'每页显示1000条'

    actions = [setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]

    def changelist_view(self, request, extra_context=None):
        """不选择object的前提下执行action
        """
        if 'action' in request.POST and 'setListPerPage' in request.POST['action']:
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in LogEntry.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(LogEntryAdmin, self).changelist_view(request, extra_context)





