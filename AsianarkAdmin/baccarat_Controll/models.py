#coding:utf8
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label] into your database.
from __future__ import unicode_literals
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from AsianarkAdmin.baccarat_Controll.memopr import memopr
from AsianarkAdmin.tools.choicecode import *
from django.utils.encoding import smart_text

class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

class TBulletin(models.Model):
    """公告信息
    """
    tomorrow = datetime.datetime.now()+datetime.timedelta(days = 1)

    bulletinid = models.AutoField(verbose_name= u'公告ID',max_length=11,primary_key=True)
    create_time = models.DateTimeField(verbose_name= u'创建时间',default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    expired_time = models.DateTimeField(verbose_name= u'到期时间',default=tomorrow) #多一天
    text = models.TextField(max_length=200,verbose_name= u'公告内容')
    flag = models.IntegerField(verbose_name= u'是否禁用',choices=FLAG,default=0)   #0:启用,1:禁用

    def __unicode__(self):
        return '公告 %s' %self.bulletinid

    class Meta:
        managed = False
        db_table = 't_bulletin'
        verbose_name = u'公告信息'
        verbose_name_plural = u'公告信息'


class TVideo(models.Model):

    videoid = models.CharField(db_column='VideoID', verbose_name= u'视频ID',primary_key=True, max_length=16,help_text=u'不要在删除桌台id前删除相应视频id')
    gametype = models.CharField(db_column='GameType', verbose_name= u'游戏类型', max_length=16,choices=GAMETYPE,default='BJL')
    flag = models.IntegerField(db_column='Flag',verbose_name= u'是否禁用',choices=FLAG,default=0)
    bettime = models.IntegerField(db_column='BetTime',verbose_name= u'下注倒计时(秒)',default=0)
    url = models.CharField(db_column='URL', max_length=160,verbose_name= u'URL')

    def changeVideoInMem(self):
        """更新视频到缓存
        """
        mdata = {'videoid':self.videoid,'url':self.url,'flag':self.flag,'bettime':self.bettime,'gametype':self.gametype}
        memopr.changeVideoInMem(mdata)

    def __unicode__(self):
        return self.videoid

    class Meta:
        managed = False
        db_table = 't_video'
        verbose_name =  u'视频信息'
        verbose_name_plural =  u'视频信息'


class TTableLimitset(models.Model):

    id = models.AutoField(primary_key=True)
    limitid = models.CharField(db_column='LimitID',verbose_name= u'限红ID',max_length=4)
    playtype = models.IntegerField(db_column='PlayType',verbose_name= u'玩法',validators=[MinValueValidator(0), MaxValueValidator(9999)])
    min_cents = models.IntegerField(db_column='Min_Cents',verbose_name= u'最小下注额度',default=0)
    max_cents = models.IntegerField(db_column='Max_Cents',verbose_name= u'最大下注额度',default=100)
    flag = models.IntegerField(db_column='Flag',verbose_name= u'是否禁用',choices=FLAG,default=0)

    def __unicode__(self):
        return  u'桌台限红 %s,%s' %(self.limitid,self.playtype)

    class Meta:
        managed = False
        db_table = 't_table_limitset'
        verbose_name =  u'桌台限红表'
        verbose_name_plural =  u'桌台限红表'


class TTable(models.Model):
    """桌台操作相关"""

    tableid = models.CharField(db_column='TableID',verbose_name= u'桌台ID', primary_key=True, max_length=16)
    videoid = models.ForeignKey(TVideo,db_column= 'VideoID',verbose_name=u'视频ID',help_text=u'不要在这里执行删除操作,最好也不要在这里添加视频')
    gametype = models.CharField(db_column='GameType',verbose_name= u'游戏类型',choices=GAMETYPE,default='BJL',max_length=16)
    limitid = models.CharField(db_column='LimitID',choices=LIMITID,verbose_name= u'限红ID',help_text=u'请与桌台限红表中数据保持一致',max_length=4)
    seats = models.IntegerField(db_column='Seats',validators=[MinValueValidator(0), MaxValueValidator(9999)],verbose_name= u'座位数',default=7)
    flag = models.IntegerField(db_column='Flag',verbose_name= u'是否禁用',choices=FLAG,default=0)

    def changeTableInMem(self):
        mdata = {'videoid':self.videoid.videoid,'gametype':self.gametype,'tableid':self.tableid,'flag':self.flag,'seats':self.seats,'limitid':self.limitid}
        memopr.changeTableInMem(mdata)

    def __unicode__(self):
        return self.tableid

    class Meta:
        managed = False
        db_table = 't_table'
        verbose_name = u'桌台信息'
        verbose_name_plural = u'桌台信息'


class TPersonalLimitset(models.Model):

    id = models.AutoField(primary_key=True)
    limitid = models.CharField(db_column='LimitID',verbose_name= u'限红ID',max_length=11)
    playtype = models.IntegerField(db_column='PlayType',verbose_name= u'玩法',validators=[MinValueValidator(0), MaxValueValidator(9999)])
    min_cents = models.IntegerField(db_column='Min_Cents', verbose_name= u'最小下注额度',default=0)
    max_cents = models.IntegerField(db_column='Max_Cents', verbose_name= u'最大下注额度',default=100)
    flag = models.IntegerField(db_column='Flag',verbose_name = u'是否禁用',choices=FLAG,default=0)

    def __unicode__(self):
        return  u'个人限红 %s,%s' %(self.limitid,self.playtype)

    class Meta:

        managed = False
        db_table = 't_personal_limitset'
        verbose_name =  u'个人限红表'
        verbose_name_plural =  u'个人限红表'


class TOrders(models.Model):


    billno = models.IntegerField(primary_key=True,verbose_name=u'注单号码')
    gametype = models.CharField(max_length=16,verbose_name=u'游戏类型',choices=GAMETYPE)
    loginname = models.CharField(max_length=32,verbose_name=u'账户名称')
    agentcode = models.IntegerField(db_column='AgentCode',verbose_name=u'代理CODE')
    roundcode = models.CharField(max_length=16,verbose_name=u'游戏局号')
    videoid = models.CharField(db_column='videoid',max_length=16,verbose_name= u'视频ID',default='')
    tableid = models.CharField(db_column='tableid',max_length=16,verbose_name= u'桌台ID',default='')
    seat = models.IntegerField(verbose_name=u'位置',validators=[MinValueValidator(0), MaxValueValidator(9999)])
    dealer = models.CharField(max_length=16,verbose_name='荷官')
    flag = models.IntegerField(db_column='Flag',verbose_name= u'结算标志',choices=ORDERFLAG,default=0)
    playtype = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)],verbose_name=u'玩法')
    bet_amount_cents = models.IntegerField(default=0,verbose_name=u'投注额')
    valid_bet_amount_cents = models.IntegerField(default=0,verbose_name=u'有效投注额')
    win_amount_cents = models.IntegerField(default=0,verbose_name=u'盈利额')
    hashcode = models.CharField(max_length=32,verbose_name='哈希值')
    before_credit_cents = models.IntegerField(db_column='Before_credit_Cents',verbose_name=u'原额度',default=0)
    after_credit_cents = models.IntegerField(db_column='After_credit_Cents',verbose_name=u'现额度',default=0)
    create_time = models.DateTimeField(db_column='Create_time',verbose_name= u'创建时间',default=datetime.datetime.now)
    reckon_time = models.DateTimeField(db_column='Reckon_time',verbose_name=u'结算时间',blank=True,null=True)
    create_ip = models.GenericIPAddressField(verbose_name= u'创建IP', max_length=16)




    def __unicode__(self):
        return '%s'%self.billno

    class Meta:
        managed = False
        db_table = 't_orders'
        verbose_name =  u'游戏注单'
        verbose_name_plural =  u'游戏注单'


class TRounds(models.Model):

    roundcode = models.CharField(primary_key=True, max_length=16,verbose_name=u'游戏局号')
    gametype = models.CharField(max_length=4,verbose_name= u'游戏类型',choices=GAMETYPE)
    videoid = models.CharField(db_column='videoid',max_length=16,verbose_name= u'视频ID')
    dealer = models.CharField(blank=True, null=True , max_length=16,verbose_name= u'荷官')
    flag = models.IntegerField(db_column= u'Flag',verbose_name= u'结算标志',choices=FLAG,default=0)
    cards = models.CharField(max_length=24, blank=True, null=True,verbose_name=u'牌值列表',help_text=u'请按照格式1,2,3:4,5,6输入')
    cardnum = models.IntegerField(blank=True, null=True,verbose_name=u'牌张数',validators=[MinValueValidator(0), MaxValueValidator(9999)])
    pair = models.IntegerField(blank=True,null=True,choices=PAIR,verbose_name=u'庄闲对',validators=[MinValueValidator(0), MaxValueValidator(9999)])
    bankerpoint = models.IntegerField(blank=True, null=True,validators=[MinValueValidator(0), MaxValueValidator(9999)],verbose_name= u'庄家点数')
    playerpoint = models.IntegerField(blank=True, null=True,validators=[MinValueValidator(0), MaxValueValidator(9999)],verbose_name= u'闲家点数')
    begintime = models.DateTimeField(verbose_name= u'开始时间',default=datetime.datetime.now)
    closetime = models.DateTimeField(blank=True, null=True,verbose_name= u'结束时间')
    shoecode = models.CharField(max_length=16,verbose_name='靴号')


    def __unicode__(self):
        return '%s'%self.roundcode

    class Meta:
        managed = False
        db_table = 't_rounds'
        verbose_name =  u'游戏局记录'
        verbose_name_plural =  u'游戏局记录'


class TRecalcRounds(models.Model):

    actionid = models.IntegerField(primary_key=True,verbose_name=u'操作ID')
    create_time = models.DateTimeField(db_column='Create_time',verbose_name= u'创建时间',default=datetime.datetime.now)
    action = models.CharField(max_length=64,verbose_name=u'操作')
    roundcode = models.CharField(max_length=16,verbose_name=u'游戏局号')

    def __unicode__(self):
        return '%s'%self.actionid

    class Meta:
        managed = False
        db_table = 't_recalc_rounds'
        verbose_name =  u'重新结算游戏局记录'
        verbose_name_plural =  u'重新结算游戏局记录'





