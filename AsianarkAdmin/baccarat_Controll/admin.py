#coding:utf8
"""
@__author__ = 'Thomas'
"""
from django.contrib import admin
from AsianarkAdmin.tools.protobuff import login_pb2,tableLimit_pb2,bulletin_pb2
import requests
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.http import HttpResponseRedirect
from django.db.models.signals import post_save
from AsianarkAdmin.baccarat_Controll.models import TBulletin,TTableLimitset,TPersonalLimitset,TRounds,TVideo,TTable,TOrders
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

    list_display = ('bulletinid','text','create_time','expired_time','flag')
    search_fields = ('bulletinid','text','flag')
    list_filter = ('create_time','expired_time','flag')
    ordering = ('-create_time','bulletinid')

    def save_model(self, request, obj, form, change):
        obj.save()


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
                reponse=requests.get('http://%s:%s/bulletin?command=%s'%(url,port,command))
            except Exception, e:
                response = HttpResponseRedirect("/admin")
                print 'Cannot send bulletin to the Game Server.'
                return response
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


@admin.register(TOrders)
class TOrdersAdmin(admin.ModelAdmin):

    def recalcRound(self, request, queryset):

        message = u"重新结算注单"
        self.message_user(request, "%s" % message)
        command = 50016
        try:
            response=requests.get('http://%s:%s/order?command=%s'%(url,port,command))
        except Exception, e:
            message = u'Cannot send recalcRound to the Game Server'
            self.message_user(request, "%s" % message)
            print message

    recalcRound.short_description = u'重新结算局注单'

    def cancelOrder(self, request, queryset):
        pass
    cancelOrder.short_description = u'取消结算局注单'


    #list_display = ()
    actions = [recalcRound,cancelOrder]


@admin.register(TRounds)
class TRoundAdmin(admin.ModelAdmin):

    list_display = ('roundcode','gametype','videoid','dealer','cards','begintime','closetime','shoecode')
    search_fields = ('roundcode','gametype','dealer','cards','shoecode')
    list_filter = ('gametype','dealer','videoid','cards','begintime','closetime')
    ordering = ('roundcode',)
    #readonly_fields = ('roundcode',)


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

    def changelist_view(self, request, extra_context=None):
        """列表页面
        The 'change list' admin view for this model.
        """
        memopr.syncVideoMemAndDb()
        return super(TVideoAdmin, self).changelist_view(request,extra_context=extra_context)

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

    list_display = ('tableid','videoid','seats','flag')
    search_fields = ('tableid','videoid','seats','flag')
    ordering = ('tableid','seats','videoid')
    list_filter = ('videoid','flag')
    readonly_fields = ('tableid',)

    def get_actions(self, request):
        """只允许特定管理者有删除桌台权限"""
        actions = super(TTableAdmin, self).get_actions(request)
        if not request.user.is_superuser or request.user.username.upper() != 'ADMIN':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def get_readonly_fields(self,request,obj=None):
        if obj:
            return ['tableid']
        else:
            return []

    def changelist_view(self, request, extra_context=None):
        """列表页面
        The 'change list' admin view for this model.
        """
        memopr.syncVideoMemAndDb()
        memopr.syncTableMemAndDb()
        return super(TTableAdmin, self).changelist_view(request,extra_context=extra_context)

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
