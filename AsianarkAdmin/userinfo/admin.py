#coding:utf8
"""
@__author__ = 'Thomas'
"""

from django.contrib import admin
from AsianarkAdmin.userinfo.models import TCustomers,TCustomerTrans,TAgents
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class DelegateFilter(admin.SimpleListFilter):

    title = 'Customers'
    parameter_name = 'loginname'

    def lookups(self, request, model_admin):
        ##loginnames = set([c.loginname for c in model_admin.modelobjs.all()])
        return [c.loginname for c in model_admin.model.objcts.all()]


@admin.register(TAgents)
class TAgentsAdmin(admin.ModelAdmin):

    def mycreate_time(self,obj):
        if not obj.create_time:
            return obj.create_time
        else:
            return obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
    mycreate_time.short_description = u'创建时间'
    mycreate_time.admin_order_field = 'create_time'

    list_display = ('agentcode','agentname','mycreate_time','create_ip','trytype','flag')
    search_fields =  ('agentcode','agentname','create_ip','trytype')
    list_filter = ('agentcode','agentname','create_ip','trytype','flag')
    ordering = ('agentcode',)

@admin.register(TCustomers)
class TCustomersAdmin(admin.ModelAdmin):

    def mycreate_time(self,obj):
        if not obj.create_time:
            return obj.create_time
        else:
            return obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
    mycreate_time.short_description = u'创建时间'
    mycreate_time.admin_order_field = 'create_time'

    def mylast_login_time(self,obj):
        if not obj.last_login_time:
            return obj.last_login_time
        else:
            return obj.last_login_time.strftime('%Y-%m-%d %H:%M:%S')
    mylast_login_time.short_description = u'最后一次登录时间'
    mylast_login_time.admin_order_field = 'last_login_time'

    def mypwd_expired_time(self,obj):
        if not obj.pwd_expired_time:
            return obj.pwd_expired_time
        else:
            return obj.pwd_expired_time.strftime('%Y-%m-%d %H:%M:%S')
    mypwd_expired_time.short_description = u'密码失效时间'
    mypwd_expired_time.admin_order_field = 'pwd_expired_time'


    readonly_fields = ('loginname','agentcode','password','nickname','credit_cents','create_time','create_ip','last_login_time','pwd_expired_time','last_login_ip')
    list_display = ('loginname','agentcode','nickname','credit_cents','limitid','mycreate_time','create_ip','mylast_login_time','last_login_ip','mypwd_expired_time','flag')
    search_fields = ('loginname','agentcode','nickname','credit_cents','limitid','create_time','create_ip','last_login_time','last_login_ip','pwd_expired_time','flag')
    list_filter = ('loginname',)
    ordering = ('-create_time','nickname',)

    def has_add_permission(self, request,obj=None):
        return False

    def has_delete_permission(self,request,obj=None):
        return False

    def get_actions(self, request):
        actions = super(TCustomersAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

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

    def get_queryset(self, request):
        """只显示代理数据
        """

        qs = super(TCustomersAdmin, self).get_queryset(request)
        inner_qs=TAgents.objects.filter(user_id=request.user.id)
        if request.user.is_superuser:
            return qs
        return qs.filter(agentcode=inner_qs)

    def changelist_view(self, request, extra_context=None):
        """不选择object的前提下执行action

        """
        if 'action' in request.POST and 'setListPerPage' in request.POST['action']:
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in TCustomers.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.loginname)})
                request._set_post(post)

        return super(TCustomersAdmin, self).changelist_view(request, extra_context)

    actions = [setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]


@admin.register(TCustomerTrans)
class TCustomerTransAdmin(admin.ModelAdmin):

    def myaction_time(self,obj):
        if not obj.action_time:
            return obj.action_time
        else:
            return obj.action_time.strftime('%Y-%m-%d %H:%M:%S')
    myaction_time.short_description = u'创建时间'
    myaction_time.admin_order_field = 'action_time'

    list_display = ('transid','loginname','agentcode','action','myaction_time','trans_amount_cents','before_credit_cents','after_credit_cents','remark')
    readonly_fields = ('transid','action_time','loginname','agentcode','action','trans_amount_cents','before_credit_cents','after_credit_cents','remark')
    search_fields =  ('transid','action_time','loginname','agentcode','action','trans_amount_cents')
    list_filter = ('loginname','action_time','agentcode','action')
    ordering = ('-transid',)

    def has_add_permission(self, request,obj=None):
        return False

    def has_delete_permission(self,request,obj=None):
        return False

    def get_actions(self, request):
        actions = super(TCustomerTransAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

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

    def changelist_view(self, request, extra_context=None):
        """不选择object的前提下执行action
        """
        if 'action' in request.POST and 'setListPerPage' in request.POST['action']:
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in TCustomerTrans.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.transid)})
                request._set_post(post)

        return super(TCustomerTransAdmin, self).changelist_view(request, extra_context)

    actions = [setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]


# class TAgentsInline(admin.StackedInline):
#     model = TAgents
#     can_delete = False
#     verbose_name = u'代理'
#
#
# class UserAdmin(UserAdmin):
#     inlines = (TAgentsInline,)
#
#
# admin.site.unregister(User)
# admin.site.register(User,UserAdmin)