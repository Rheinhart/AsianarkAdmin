#coding:utf8
from django.db import models
from django.contrib import admin
import hashlib
from django.contrib.auth.models import User
from time import strftime
import datetime

class TControllers(models.Model):

    """自定义后台管理员信息
       权限 permit 1 后台管理员
       权限 permit 2 现场管理员
    """
    PERMIT = ((1,u'后台管理员'),
              (2,u'现场管理员'),)

    FLAG = ((0,u'启用'),(1,u'禁用'),)

    PASS_KEY = strftime("%Y%m%d%H%M%S")

    user = models.OneToOneField(User) #自定义User model

    loginname = models.CharField(db_column='Loginname', verbose_name='用户名',unique=True, primary_key=True, max_length=16)  # Field name made lowercase.
    password = models.CharField(max_length=32,verbose_name='密码')
    permit = models.IntegerField(choices=PERMIT,verbose_name='操作权限',default=1)
    flag = models.IntegerField(choices=FLAG,verbose_name='是否禁用',default=0)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            TControllers.objects.create(user=instance)

    #post_save.connect(create_user_profile, sender=User)

    def serializable_password(self):
        '''加密密码
        '''
        sha = hashlib.md5()
        sha.update(self.password+self.PASS_KEY+self.loginname)
        self.password = sha.hexdigest().upper()

    def check_password(self,password):
        '''检测密码
        '''
        sha = hashlib.md5()
        sha.update(password+self.PASS_KEY+self.loginname)
        nowpassword = sha.hexdigest().upper()
        if nowpassword==self.password:
            return True
        return False

    def __unicode__(self):
        """
        """
        return "loginname=%s permit=%s flag=%s"%(self.loginname,self.permit,self.flag)

    class Meta:

        verbose_name = u'管理员表'
        verbose_name_plural = u'管理员表'
        managed = False
        db_table = 't_controllers'

class TControllerlog(models.Model):
    loginname = models.CharField(db_column='Loginname',verbose_name='操作log', primary_key=True, max_length=16)  # Field name made lowercase.
    action = models.CharField(db_column='Action', verbose_name='操作', max_length=64)  # Field name made lowercase.
    action_time = models.DateTimeField(db_column='Action_time',verbose_name='操作开始时间',default=datetime.datetime.now) # Field name made lowercase.
    remark = models.CharField(max_length=100,verbose_name='记录')

    class Meta:
        managed = False
        db_table = 't_controllerlog'
        verbose_name= u"控制器操作记录表"
        verbose_name_plural = u'控制器操作记录表'


#@admin.register(TControllers)
class ControllersAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.serializable_password()
        obj.save()
