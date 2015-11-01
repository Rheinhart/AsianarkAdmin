#coding:utf8
"""
@__author__ = 'Thomas'
"""

from django.contrib import admin
from AsianarkAdmin.userinfo.models import TCustomers,TCustomerTrans

@admin.register(TCustomers)
class TCustomersAdmin(admin.ModelAdmin):
    list_display = ('loginname','nickname','credit_cents','limitid','create_time','create_ip','last_login_time','last_login_ip','pwd_expired_time','flag')

@admin.register(TCustomerTrans)
class TRoundAdmin(admin.ModelAdmin):
    list_display = ('transid','action_time','loginname')

