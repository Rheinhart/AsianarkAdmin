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
from AsianarkAdmin.Baccarat_Livel.models import TBulletin,TTableLimitset,TPersonalLimitset,TRounds,TVideo,TTable
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
    search_fields = ('bulletinid','flag')

    def save_model(self, request, obj, form, change):
        obj.save()
        #obj.pushBulletinToGameSer()

@receiver(post_save, sender=TBulletin)
def pushBulletinToGameSer(sender,instance,**argvs):
        """push bulletin to the gameserver after which saved into the database
        """
        command = 20037

        #mybulletin = bulletin_pb2.bulletinResponse()
        #mybulletin.beginTime = instance.create_time.strftime("%Y-%m-%d %H:%M:%S")
        #mybulletin.endTime = instance.expired_time.strftime("%Y-%m-%d %H:%M:%S")
        #mybulletin.text = instance.text
        try:
            requests.get('http://%s:%s/bulletin?command=%s'%(url,port,command))
        except Exception, e:
            response = HttpResponseRedirect("/admin")
            return response

@admin.register(TTableLimitset)
class TTableLimitsetAdmin(admin.ModelAdmin):

    list_display = ('limitid','playtype','min_cents','max_cents','flag')

@receiver(post_save, sender=TTableLimitset)
def pushTableLimitToGameSer(instance,**argvs):
    """push TableLimit message to the gameserver after which saved into the database
    """
    mytableLimit = tableLimit_pb2.tableLimit()
    mytableLimit.limitid = instance.limitid
    mytableLimit.playtype = instance.playtype
    mytableLimit.min = instance.min
    mytableLimit.max = instance.max
    mytableLimit.flag = instance.flag

    return requests.post('%s:%s'%(url,port),mytableLimit.SerializeToString())

@admin.register(TPersonalLimitset)
class TPersonalLimitsetAdmin(admin.ModelAdmin):

    list_display = ('limitid','playtype','min_cents','max_cents','flag')
    search_fields = ('limitid','playtype','min_cents','max_cents','flag')


@admin.register(TRounds)
class TRoundAdmin(admin.ModelAdmin):

    list_display = ('roundcode','gametype','videoid','dealer','cards','begintime','closetime','shoecode')

@admin.register(TVideo)
class TVideoAdmin(admin.ModelAdmin):

    list_display = ('videoid','gametype','bettime','url','flag')
    search_fields = ('videoid','gametype','bettime','url','flag')
    ordering = ('videoid',)
    readonly_fields = ('videoid',)

    def get_actions(self, request):
        """只允许特定管理者有删除视频权限"""
        actions = super(TVideoAdmin, self).get_actions(request)
        if not request.user.is_superuser or request.user.username.upper() != 'ADMIN':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

        #def mem_refresh(self, request, queryset):
        #updateVideoMemToDb()
        #mem_refresh.short_description = u'更新所有的视频信息表'

    def get_readonly_fields(self,request,obj=None):
        if obj:
            return ['videoid']
        else:
            return []

    def changelist_view(self, request, extra_context=None):
        """列表页面
        The 'change list' admin view for this model.
        """
        memopr.syncVideoMemToDb()
        return super(TVideoAdmin, self).changelist_view(request,extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if change: #change
            #obj_old = self.model.objects.get(pk=obj.pk)
            print 'change:In memcached'
            obj.change_video()
        else: #add
            print 'add:Database to memcached'
            obj.save()
            obj.add_video()

@admin.register(TTable)
class TTableAdmin(admin.ModelAdmin):

    ordering = ('tableid',)
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
        memopr.syncVideoMemToDb()
        memopr.syncTableMemToDb()
        return super(TTableAdmin, self).changelist_view(request,extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if change: #change,在修改页面
            #obj_old = self.model.objects.get(pk=obj.pk)
            print 'change: Mem'
            obj.change_table()
        else: #add,在添加页面
            print 'add:Db to Mem'
            obj.save()
            obj.add_table()

#def getVideoInfoFromGameSer(**kwargs):
#    command = 50002
#    try:
#        requests.get('%s:%s/video?command=%s'%(url,port,command))
#    except Exception, e:
#        response = HttpResponseRedirect("/admin")
#        return response
