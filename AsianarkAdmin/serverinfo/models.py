#coding:utf8
"""
@__author__ = 'Thomas'
"""
from django.db import models
from django.contrib import admin
import datetime

class TAgents(models.Model):
    agentcode = models.IntegerField(db_column='AgentCode', primary_key=True)
    agentname = models.CharField(db_column='AgentName', max_length=32)
    password = models.CharField(db_column='Password',max_length=32)
    flag = models.IntegerField(db_column='Flag')
    trytype = models.IntegerField(db_column='Try_Type')
    create_time = models.DateTimeField(db_column='Create_time',default=datetime.datetime.now)
    create_ip = models.GenericIPAddressField(db_column='Create_ip',verbose_name= u'创建IP', max_length=16)

    class Meta:
        managed = False
        db_table = 't_agents'
        verbose_name = u'代理信息'
        verbose_name_plural = u'代理信息'


@admin.register(TAgents)
class TRoundAdmin(admin.ModelAdmin):
    list_display = ('agentcode','agentname')
