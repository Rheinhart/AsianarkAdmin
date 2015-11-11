#coding:utf8
"""
@__author__ = 'Thomas'
"""
from django.contrib import admin
from django import forms
from AsianarkAdmin.tools.protobuff import login_pb2,tableLimit_pb2,bulletin_pb2
import requests
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.http import HttpResponseRedirect
from django.db.models.signals import post_save
from AsianarkAdmin.baccarat_Controll.models import TBulletin,TTableLimitset,TPersonalLimitset,TRounds,TRecalcRounds,TVideo,TTable,TOrders
from AsianarkAdmin.settings import GAME_SERVER
from memopr import memopr

url =  GAME_SERVER['dafault'].get('URL')
port = GAME_SERVER['dafault'].get('PORT')

@receiver(user_logged_in)
def pushLoginMessageToGameSer(**kwargs):
        """push message to the gameserver when login
           code: 0x00050002
        """
        #login = login_pb2.loginResultResponse()
        #login.code = 0x00050002
        #login.token = '123456'
        #login.flag = 2
        try:
            requests.get('http//%s:%s/clogin'%(url,port))

        except Exception,e:
            print "Cannot send message to Game Server"
            response = HttpResponseRedirect("/admin")
            return response

@admin.register(TBulletin)
class TBulletinAdmin(admin.ModelAdmin):

    list_display = ('bulletinid','text','mycreate_time','myexpired_time')
    search_fields = ('bulletinid','text')
    list_filter = ('create_time','expired_time')
    ordering = ('-create_time','bulletinid')
    readonly_fields = ('create_time','flag')

    def save_model(self, request, obj, form, change):
        obj.save()

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
                for u in TBulletin.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.bulletinid)})
                request._set_post(post)
        return super(TBulletinAdmin, self).changelist_view(request, extra_context)

    actions = [setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]


@receiver(post_save, sender=TBulletin)
def pushBulletinToGameSer(sender,instance,**argvs):
    """push new bulletin to the gameserver after which saved into the database
    """
        #mybulletin = bulletin_pb2.bulletinResponse()
        #mybulletin.beginTime = instance.create_time.strftime("%Y-%m-%d %H:%M:%S")
        #mybulletin.endTime = instance.expired_time.strftime("%Y-%m-%d %H:%M:%S")
        #mybulletin.text = instance.text
    command = 50013
    if instance.flag == 0:
        try:
            response=requests.get('http://%s:%s/bulletin?command=%s'%(url,port,command))
            if response.content == '60013':
                message = response.content
                print 'code:%s'%message
        except Exception, e:
            response = HttpResponseRedirect("/admin")
            print 'Cannot send bulletin to the Game Server.'
            return response.content
    else:
        return HttpResponseRedirect("/admin")



@admin.register(TTableLimitset)
class TTableLimitsetAdmin(admin.ModelAdmin):

    list_display = ('limitid','playtype','min_cents','max_cents','flag')
    search_fields = ('limitid','playtype','min_cents','max_cents','flag')
    list_filter = ('limitid','playtype','min_cents','max_cents','flag')


@receiver(post_save, sender=TTableLimitset)
def pushTableLimitToGameSer(instance,**argvs):
    """push TableLimit message to the gameserver after which saved into the database
    """
    mytableLimit = tableLimit_pb2.tableLimit()
    mytableLimit.limitid = instance.limitid
    mytableLimit.playtype = instance.playtype
    mytableLimit.minval = instance.min_cents
    mytableLimit.maxval = instance.max_cents

    try:
        reponse=requests.post('%s:%s'%(url,port),mytableLimit.SerializeToString())
    except Exception, e:
            response = HttpResponseRedirect("/admin/baccarat_Controll/ttablelimitset")
            print 'Cannot send TableLimit to the Game Server.'
            return response


@admin.register(TPersonalLimitset)
class TPersonalLimitsetAdmin(admin.ModelAdmin):

    list_display = ('limitid','playtype','min_cents','max_cents','flag')
    search_fields = ('limitid','playtype','min_cents','max_cents','flag')
    list_filter = ('limitid','playtype','min_cents','max_cents','flag')
    #list_editable=('limitid','playtype','min_cents','max_cents','flag')


@admin.register(TOrders)
class TOrdersAdmin(admin.ModelAdmin):

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
                for u in TOrders.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.billno)})
                request._set_post(post)
        return super(TOrdersAdmin, self).changelist_view(request, extra_context)


    list_display = ('billno','roundcode','loginname','agentcode','gametype','videoid','tableid','seat','dealer','flag','playtype',
                    'bet_amount_cents','win_amount_cents','valid_bet_amount_cents','before_credit_cents','after_credit_cents','mycreate_time',
                    'myreckon_time','create_ip')
    readonly_fields = ('billno','gametype','loginname','agentcode','roundcode','videoid','tableid','seat','dealer','flag','playtype',
                    'bet_amount_cents','win_amount_cents','valid_bet_amount_cents','before_credit_cents','after_credit_cents','create_time',
                    'reckon_time','create_ip','hashcode')
    search_fields = ('billno','loginname','agentcode','roundcode','videoid','tableid','create_time','reckon_time',)
    list_filter = ('create_time','reckon_time','flag')
    ordering = ('-create_time','-billno')

    def has_add_permission(self, request,obj=None):
        return False

    def has_delete_permission(self,request,obj=None):
        return False

    def has_add_permission(self, request,obj=None):
        return False

    def get_actions(self, request):
        actions = super(TOrdersAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    actions = [setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]



@admin.register(TRounds)
class TRoundAdmin(admin.ModelAdmin):
    """游戏局记录管理
    """
    list_display = ('roundcode','gametype','flag','videoid','dealer','cards','cardnum','pair','bankerpoint','playerpoint','mybegintime','myclosetime','shoecode')
    search_fields = ('roundcode','gametype','flag','dealer','cards','shoecode')
    list_filter = ('gametype','dealer','videoid','flag','cards','begintime','closetime')
    ordering = ('-roundcode',)
    readonly_fields = ('roundcode','gametype','flag','videoid','dealer','cards','cardnum','pair','bankerpoint','playerpoint','begintime','closetime','shoecode',)

    def recalcRound(self, request, queryset):
        head = u"重新结算局"
        command = 50016
        try:
            if len(queryset) == 1:
                roundcode = queryset[0].roundcode
                flag = queryset[0].flag
                if flag == 0:
                    response=requests.get('http://%s:%s/order?command=%s&roundcode=%s'%(url,port,command,roundcode))
                    if response.content == '60016':
                        message = u'结算成功'
                    else:
                         message = u'结算失败'
                    self.message_user(request, "%s: %s%s" %(head,roundcode,message))
                else:
                    message = u'已经结算过'
                    self.message_user(request, "%s: %s%s" %(head,roundcode,message))
            else:
                message = u'只能选择一局结算'
                self.message_user(request, "%s: %s" %(head,message))
        except Exception, e:
            message = u'发送指令出错'
            self.message_user(request, "%s: %s" %(head,message))
    recalcRound.short_description = u'重新结算局'

    def cancelRound(self, request, queryset):
        head = u"取消局注单结算"
        command = 50017
        try:
            if len(queryset) == 1:
                roundcode = queryset[0].roundcode
                flag = queryset[0].flag
                if flag == 0:
                    response=requests.get('http://%s:%s/order?command=%s&roundcode=%s'%(url,port,command,roundcode))
                    if response.content == '60017':
                        message = u'取消成功'
                    else:
                        message = u'取消失败'
                    self.message_user(request, "%s: %s%s" %(head,roundcode,message))
            else:
                message = u'只能取消一局'
                self.message_user(request, "%s: %s" %(head,message))
        except Exception, e:
            message = u'发送指令出错'
            self.message_user(request, "%s:%s" %(head,message))
    cancelRound.short_description = u'取消局注单结算'

    def has_add_permission(self, request,obj=None):
        return False

    def has_delete_permission(self,request,obj=None):
        return False

    def get_actions(self, request):
        actions = super(TRoundAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        obj.save()

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
                for u in TRounds.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.roundcode)})
                request._set_post(post)
        return super(TRoundAdmin, self).changelist_view(request, extra_context)

    actions = [recalcRound,cancelRound,setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]



@admin.register(TRecalcRounds)
class TRecalcRoundsAdmin(admin.ModelAdmin):
    list_display = ('actionid','action','mycreate_time','roundcode')
    search_fields = ('actionid','create_time','action','roundcode')
    list_filter = ('actionid','action','create_time','roundcode')
    ordering = ('-actionid',)
    readonly_fields = ('actionid','action','create_time','roundcode')

    def has_add_permission(self, request,obj=None):
        return False

    def has_delete_permission(self,request,obj=None):
        return False

    def get_actions(self, request):
        actions = super(TRecalcRoundsAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        obj.save()

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
                for u in TRecalcRounds.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.actionid)})
                request._set_post(post)
        return super(TRecalcRoundsAdmin, self).changelist_view(request, extra_context)

    actions = [setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]



@admin.register(TVideo)
class TVideoAdmin(admin.ModelAdmin):

    list_display = ('videoid','gametype','bettime','url','flag')
    search_fields = ('videoid','gametype','bettime','url','flag')
    list_filter = ('videoid','gametype','bettime','url','flag')
    ordering = ('videoid',)
    readonly_fields = ('videoid',)

    def get_actions(self, request):
        """只允许特定管理者有删除视频权限"""
        actions = super(TVideoAdmin, self).get_actions(request)
        if not request.user.is_superuser or request.user.username.upper() != 'ADMIN':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def get_readonly_fields(self,request,obj=None):
        if obj:
            return ['videoid']
        else:
            return []

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
                for u in TVideo.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.videoid)})
                request._set_post(post)

        memopr.syncVideoMemAndDb()
        return super(TVideoAdmin, self).changelist_view(request, extra_context)

    actions = [setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]

    def save_model(self, request, obj, form, change):
        if change: #change
            #obj_old = self.model.objects.get(pk=obj.pk)
            print 'change'
            obj.change_video()
        else: #add
            print 'add'
            obj.save()


@admin.register(TTable)
class TTableAdmin(admin.ModelAdmin):

    list_display = ('tableid','videoid','limitid','seats','flag')
    search_fields = ('tableid','videoid','limitid','seats','flag')
    ordering = ('tableid','seats','videoid')
    list_filter = ('videoid','flag','limitid','seats')
    readonly_fields = ('gametype',)

    def get_actions(self, request):
        """只允许特定管理者有删除桌台权限"""
        actions = super(TTableAdmin, self).get_actions(request)
        if not request.user.is_superuser or request.user.username.upper() != 'ADMIN':
            if 'delete_selected' in actions:
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
                for u in TTable.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.tableid)})
                request._set_post(post)

        memopr.syncVideoMemAndDb()
        memopr.syncTableMemAndDb()
        return super(TTableAdmin, self).changelist_view(request, extra_context)

    actions = [setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]

    def save_model(self, request, obj, form, change):
        if change: #change,在修改页面
            print 'change'
            obj.change_table()
        else: #add,在添加页面
            print 'add'
            obj.save()


#def getVideoInfoFromGameSer(**kwargs):
#    command = 50002
#    try:
#        requests.get('%s:%s/video?command=%s'%(url,port,command))
#    except Exception, e:
#        response = HttpResponseRedirect("/admin")
#        return response
