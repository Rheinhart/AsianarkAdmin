#coding:utf8
"""
@__author__ = 'Thomas'
"""
from django.db import models
import datetime

class TCustomers(models.Model):

    FLAG = ((0,u'启用'),(1,u'禁用'),)
    LIMITID=(('A','A'),('B','B'),('C','C'),('D','D'))

    loginname = models.CharField(db_column='Loginname',verbose_name= u'用户名', max_length=32,primary_key=True)
    agentcode = models.IntegerField(db_column='AgentCode',verbose_name= u'代理CODE')
    password = models.CharField(max_length=32,verbose_name= u'密码')
    nickname = models.CharField(max_length=32,verbose_name= u'昵称')
    flag = models.IntegerField(db_column='Flag',verbose_name= u'是否禁用',choices=FLAG,default=0)
    credit_cents = models.IntegerField(db_column='Credit_cents',verbose_name=u'信用额度')
    limitid = models.CharField(db_column='limitID',choices=LIMITID,verbose_name= u'个人限红ID',max_length=4)
    create_time = models.DateTimeField(db_column='Create_time',verbose_name= u'创建时间',default=datetime.datetime.now)
    create_ip = models.GenericIPAddressField(db_column='Create_ip', max_length=16,verbose_name=u'创建IP')
    last_login_time = models.DateTimeField(db_column='Last_login_time',verbose_name= u'最后一次登录时间')
    last_login_ip = models.GenericIPAddressField(db_column='Last_login_ip',verbose_name= u'最有一次登录IP', max_length=16)
    pwd_expired_time = models.DateTimeField(db_column='Pwd_expired_time',verbose_name= u'密码失效时间')

    def mycreate_time(self):
        if not self.create_time:
            return self.create_time
        else:
            return self.create_time.strftime('%Y-%m-%d %H:%M:%S')
    mycreate_time.short_description = u'创建时间'

    def mylast_login_time(self):
        if not self.last_login_time:
            return self.last_login_time
        else:
            return self.last_login_time.strftime('%Y-%m-%d %H:%M:%S')
    mylast_login_time.short_description = u'最后一次登录时间'

    def mypwd_expired_time(self):
        if not self.pwd_expired_time:
            return self.pwd_expired_time
        else:
            return self.pwd_expired_time.strftime('%Y-%m-%d %H:%M:%S')
    mypwd_expired_time.short_description = u'密码失效时间'


    def __unicode__(self):
        '''
        '''
        return  u'用户 %s' %self.nickname

    class Meta:
        managed = False
        db_table = 't_customers'
        verbose_name =  u'用户信息'
        verbose_name_plural =  u'用户信息'


class TCustomerTrans(models.Model):

    transid = models.IntegerField(primary_key=True,verbose_name=u'序列号')
    action_time = models.DateTimeField(db_column='Action_time',verbose_name=u'操作执行时间',default=datetime.datetime.now)
    loginname = models.CharField(max_length=16,verbose_name=u"用户名")
    agentcode = models.CharField(db_column='AgentCode',verbose_name= u'代理CODE',max_length=16)
    action = models.CharField(max_length=32,verbose_name=u'操作')
    trans_amount_cents = models.IntegerField(db_column='Trans_amount_Cents',verbose_name=u'转账转额度')
    before_credit_cents = models.IntegerField(db_column='Before_credit_Cents',verbose_name=u'操作前额度')
    after_credit_cents = models.IntegerField(db_column='After_credit_Cents',verbose_name=u'操作后额度')
    remark = models.CharField(max_length=100,verbose_name=u'附注')

    def myaction_time(self):
        if not self.action_time:
            return self.action_time
        else:
            return self.action_time.strftime('%Y-%m-%d %H:%M:%S')
    myaction_time.short_description = u'操作执行时间'

    def __unicode__(self):
        '''
        '''
        return  '%s' %self.transid

    class Meta:
        managed = False
        db_table = 't_customer_trans'
        verbose_name =  u'用户额度记录'
        verbose_name_plural =  u'用户额度记录'


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


