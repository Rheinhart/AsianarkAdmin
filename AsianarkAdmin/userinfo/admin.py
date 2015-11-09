#coding:utf8
"""
@__author__ = 'Thomas'
"""

from django.contrib import admin
from AsianarkAdmin.userinfo.models import TCustomers,TCustomerTrans,TAgents

class DelegateFilter(admin.SimpleListFilter):

    title = 'Customers'
    parameter_name = 'loginname'

    def lookups(self, request, model_admin):
        ##loginnames = set([c.loginname for c in model_admin.modelobjs.all()])
        return [c.loginname for c in model_admin.model.objcts.all()]


@admin.register(TCustomers)
class TCustomersAdmin(admin.ModelAdmin):

    readonly_fields = ('loginname','agentcode','password','nickname','credit_cents','create_time','create_ip','last_login_time','pwd_expired_time','last_login_ip')
    list_display = ('loginname','agentcode','nickname','credit_cents','limitid','mycreate_time','create_ip','mylast_login_time','last_login_ip','mypwd_expired_time','flag')
    search_fields = ('loginname','agentcode','nickname','credit_cents','limitid','create_time','create_ip','last_login_time','last_login_ip','pwd_expired_time','flag')
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
class TRoundAdmin(admin.ModelAdmin):
    list_display = ('transid','loginname','agentcode','action','myaction_time','trans_amount_cents','before_credit_cents','after_credit_cents','remark')
    readonly_fields = ('transid','action_time','loginname','agentcode','action','trans_amount_cents','before_credit_cents','after_credit_cents','remark')
    search_fields =  ('transid','action_time','loginname','agentcode','action','trans_amount_cents')
    list_filter = ('action_time','agentcode','action')
    ordering = ('-transid',)

    def has_add_permission(self, request,obj=None):
        return False

    def has_delete_permission(self,request,obj=None):
        return False

    def get_actions(self, request):
        actions = super(TRoundAdmin, self).get_actions(request)
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

        return super(TRoundAdmin, self).changelist_view(request, extra_context)

    actions = [setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]


@admin.register(TAgents)
class TRoundAdmin(admin.ModelAdmin):
    list_display = ('agentcode','agentname')