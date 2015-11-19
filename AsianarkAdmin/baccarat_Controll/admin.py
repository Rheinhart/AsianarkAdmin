#coding:utf8
"""
@__author__ = 'Thomas'
"""
from django.contrib import admin
import requests
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.http import HttpResponseRedirect
from AsianarkAdmin.baccarat_Controll.models import TBulletin,TTableLimitset,TPersonalLimitset,TRounds,TRecalcRounds,TVideo,TTable,TOrders
from AsianarkAdmin.baccarat_Controll.forms import TBulletinForm
from AsianarkAdmin.settings import GAME_SERVER
from memopr import memopr

url =  GAME_SERVER['dafault'].get('URL')
port = GAME_SERVER['dafault'].get('PORT')

@receiver(user_logged_in)
def pushLoginMessageToGameSer(**kwargs):
    """push message to the gameserver when login
       code: 0x00050002
    """
    command = 50001
    data = {'controller':kwargs['user']}
    try:
        response=requests.get('http://%s:%s/controller?command=%s'%(url,port,command),data)
        if response.content == '60001':
            print 'Game Server received.'
    except Exception, e:
            print "Cannot send message to Game Server"
            response = HttpResponseRedirect("/admin")
            return response


@admin.register(TBulletin)
class TBulletinAdmin(admin.ModelAdmin):
    form = TBulletinForm

    def mycreate_time(self,obj):
        if not obj.create_time:
            return obj.create_time
        else:
            return obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
    mycreate_time.short_description = u'创建时间'
    mycreate_time.admin_order_field = 'create_time'

    def myexpired_time(self,obj):
        if not obj.expired_time:
            return obj.expired_time
        else:
            return obj.expired_time.strftime('%Y-%m-%d %H:%M:%S')
    myexpired_time.short_description = u'到期时间'
    myexpired_time.admin_order_field = 'create_time'

    list_display = ('bulletinid','text','mycreate_time','myexpired_time')
    search_fields = ('bulletinid','text')
    list_filter = ('create_time','expired_time')
    ordering = ('-bulletinid',)
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


@admin.register(TVideo)
class TVideoAdmin(admin.ModelAdmin):

    list_display = ('videoid','gametype','bettime','url','flag')
    search_fields = ('videoid','gametype','bettime','url','flag')
    list_filter = ('videoid','gametype','bettime','url','flag')
    ordering = ('videoid',)
    readonly_fields = ('videoid','bettime')

    def get_actions(self, request):
        """只允许特定管理者有删除视频权限"""
        actions = super(TVideoAdmin, self).get_actions(request)
        if not request.user.is_superuser or request.user.username.upper() != 'ADMIN':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def get_readonly_fields(self,request,obj=None):
        if obj:
            return ['videoid',]
        else:
            return []

    def delVideoAndPushToGamSer(self, request, queryset):
        videos = []
        for obj in queryset:
            videos.append(obj.videoid)
            super(TVideoAdmin,self).log_deletion(request, obj, obj.videoid) #自定义删除动作记录到log中
            obj.delete()

        command = 50005
        data = videos
        try:
            response=requests.get('http://%s:%s/video?command=%s'%(url,port,command),data)
            if response.content == '60005':
                message = u'删除视频通知服务器成功'
                self.message_user(request, "%s" %(message))
        except Exception, e:
            response = HttpResponseRedirect("/admin/baccarat_Controll/tvideo")
            message = u'通知服务器出错'
            self.message_user(request, "%s" %(message))
            return response
    delVideoAndPushToGamSer.short_description = u'删除所选视频并通知游戏服务器'

    def pushVideoInfoToGameSer(self,request,obj,command):
        """推送更新视频消息到游戏服务器
        """
        data = {'videoid':obj.videoid,'url':obj.url,'flag':obj.flag,'bettime':obj.bettime,'gametype':obj.gametype}
        try:
            response=requests.get('http://%s:%s/video?command=%s'%(url,port,command),data)
            if response.content == '60003':
                message = u'添加新视频通知服务器成功'
            elif response.content == '60004':
                message = u'修改视频通知服务器成功'
            self.message_user(request, "%s" %(message))
        except Exception, e:
            response = HttpResponseRedirect("/admin")
            message = u'通知服务器出错'
            self.message_user(request, "%s" %(message))
            return response


    def changelist_view(self, request, extra_context=None):
        """不选择object的前提下执行action
        """
        if 'action' in request.POST and 'setListPerPage' in request.POST['action']:
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in TVideo.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.videoid)})
                request._set_post(post)

        memopr.syncVideoMemAndDb() #此时同步缓存数据库
        super(TVideoAdmin,self).log_change(request, TVideo.objects.first(), u'自动同步所有视频缓存数据库')
        return super(TVideoAdmin, self).changelist_view(request, extra_context)

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

    actions = [delVideoAndPushToGamSer,setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]

    def save_model(self, request, obj, form, change):
        if change: #change
            obj.changeVideoInMem() #直接修改缓存
            self.pushVideoInfoToGameSer(request,obj,50004)
        else: #add
            obj.save() #先保存到数据库
            obj.changeVideoInMem()# 修改缓存
            self.pushVideoInfoToGameSer(request,obj,50003)


@admin.register(TTable)
class TTableAdmin(admin.ModelAdmin):

    list_display = ('tableid','videoid','limitid','seats','flag')
    search_fields = ('tableid','videoid','limitid','seats','flag')
    ordering = ('tableid','seats','videoid')
    list_filter = ('tableid','videoid','flag','limitid','seats')
    #list_filter = ('videoid','flag','limitid','seats')
    readonly_fields = ('gametype',)

    def get_actions(self, request):
        """只允许特定管理者有删除桌台权限"""
        actions = super(TTableAdmin, self).get_actions(request)
        if not request.user.is_superuser or request.user.username.upper() != 'ADMIN':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def pushTableInfoToGameSer(self,request,obj,command):
        """推送更新桌台消息到游戏服务器
        """
        data = {'videoid':obj.videoid.videoid,'gametype':obj.gametype,'tableid':obj.tableid,'flag':obj.flag,'seats':obj.seats,'limitid':obj.limitid}
        try:
            response=requests.get('http://%s:%s/table?command=%s'%(url,port,command),data)
            if response.content == '60006':
                message = u'添加新桌台通知服务器成功'
            elif response.content == '60007':
                message = u'修改桌台通知服务器成功'
            self.message_user(request, "%s" %(message))

        except Exception, e:
            response = HttpResponseRedirect("/admin")
            message = u'通知服务器出错'
            self.message_user(request, "%s" %(message))
            return response

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
        super(TTableAdmin,self).log_change(request, TTable.objects.first(), u'自动同步所有桌台和视频缓存数据库')
        return super(TTableAdmin, self).changelist_view(request, extra_context)

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

    actions = [setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]

    def save_model(self, request, obj, form, change):
        if change: #change,在修改页面
            obj.changeTableInMem()
            self.pushTableInfoToGameSer(request,obj,50007)
        else: #add,在添加页面
            obj.save()
            obj.changeTableInMem()
            self.pushTableInfoToGameSer(request,obj,50006)


@admin.register(TTableLimitset)
class TTableLimitsetAdmin(admin.ModelAdmin):

    list_display = ('limitid','playtype','min_cents','max_cents','flag')
    search_fields = ('limitid','playtype','min_cents','max_cents','flag')
    list_filter = ('limitid','playtype','min_cents','max_cents','flag')

@receiver(post_save, sender=TTableLimitset)
def pushTableLimitToGameSer(instance,**argvs):

    command = 50009
    data = {'playtaye':instance.playtype,'minval_cents':instance.min_cents,'maxval_cents':instance.max_cents,'limitid':instance.limitid,'flag':instance.flag}
    try:
        response=requests.get('http://%s:%s/tablelimit?command=%s'%(url,port,command),data)
        if response.content == '60009':
            print 'Send message to the Game Server successfully.'
    except Exception, e:
            response = HttpResponseRedirect("/admin/baccarat_Controll/tablelimitset")
            print 'Cannot send TTableLimitset to the Game Server.'
    return response.content


@admin.register(TPersonalLimitset)
class TPersonalLimitsetAdmin(admin.ModelAdmin):

    list_display = ('limitid','playtype','min_cents','max_cents','flag')
    search_fields = ('limitid','playtype','min_cents','max_cents','flag')
    list_filter = ('limitid','playtype','min_cents','max_cents','flag')
    #list_editable=('limitid','playtype','min_cents','max_cents','flag')

@receiver(post_save, sender=TPersonalLimitset)
def pushPersonalLimitToGameSer(instance,**argvs):
    """push TPersonalLimit message to the gameserver after which saved into the database
    """
    command = 50011
    data = {'playtaye':instance.playtype,'minval_cents':instance.min_cents,'maxval_cents':instance.max_cents,'limitid':instance.limitid,'flag':instance.flag}
    try:
        response=requests.get('http://%s:%s/personallimit?command=%s'%(url,port,command),data)
        if response.content == '60011':
            print 'Send message to the Game Server successfully.'
    except Exception, e:
            response = HttpResponseRedirect("/admin/baccarat_Controll/tpersonallimitset")
            print 'Cannot send PersonalLimitset to the Game Server.'
    return response.content


@admin.register(TOrders)
class TOrdersAdmin(admin.ModelAdmin):

    def mycreate_time(self,obj):
        if not obj.create_time:
            return obj.create_time
        else:
            return obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
    mycreate_time.short_description = u'创建时间'
    mycreate_time.admin_order_field = 'create_time'

    def myreckon_time(self,obj):
        if not obj.reckon_time:
            return obj.reckon_time
        else:
            return obj.reckon_time.strftime('%Y-%m-%d %H:%M:%S')
    myreckon_time.short_description = u'结算时间'
    myreckon_time.admin_order_field = 'reckon_time'


    list_display = ('loginname','billno','roundcode','gametype','videoid','tableid','seat','dealer','flag','playtype',
                    'bet_amount_cents','win_amount_cents','valid_bet_amount_cents','before_credit_cents','after_credit_cents','mycreate_time',
                    'myreckon_time','create_ip','agentcode')
    readonly_fields = ('loginname','billno','gametype','agentcode','roundcode','videoid','tableid','seat','dealer','flag','playtype',
                    'bet_amount_cents','win_amount_cents','valid_bet_amount_cents','before_credit_cents','after_credit_cents','create_time',
                    'reckon_time','create_ip','hashcode')
    search_fields = ('billno','loginname','agentcode','roundcode','videoid','tableid','create_time','reckon_time',)
    list_filter = ('loginname','create_time','reckon_time','flag')
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

    actions = [setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]

    def changelist_view(self, request, extra_context=None):
        """不选择object的前提下执行action
        """

        #统计功能
        all_orders=TOrders.objects.all()
        valid_bet_list = all_orders.values_list('valid_bet_amount_cents', flat=True)
        win_bet_list =  all_orders.values_list('win_amount_cents', flat=True)

        bet_amount_small =sum(all_orders[:admin.ModelAdmin.list_per_page].values_list('bet_amount_cents', flat=True)) #小计当前页投注额
        valid_bet_amount_small = sum(valid_bet for valid_bet in valid_bet_list[:admin.ModelAdmin.list_per_page] if valid_bet is not None) #小计有效投注额

        bet_number_total = TOrders.objects.count() #总计投注笔数
        bet_amount_total =sum(all_orders.values_list('bet_amount_cents', flat=True)) #总计投注额
        valid_bet_amount_total = sum(valid_bet for valid_bet in valid_bet_list if valid_bet is not None) #总计有效投注额

        win_amount_total = sum(win_bet for win_bet in win_bet_list if win_bet is not None) #总计盈利
        earnings_rate = float(win_amount_total) / valid_bet_amount_total *100 #盈利率


        extra_context = {'bet_amount_small':bet_amount_small,'valid_bet_amount_small':valid_bet_amount_small,
                         'bet_number_total':bet_number_total,'bet_amount_total':bet_amount_total,'valid_bet_amount_total':valid_bet_amount_total,
                         'win_amount_total':win_amount_total,'earnings_rate':earnings_rate}

        self.change_list_template = 'admin/%s/%s/change_list.html' % (TOrders._meta.app_label, 'TOrders') #for Linux! error because chinese verbose name

        #设置无选翻页func
        if 'action' in request.POST and 'setListPerPage' in request.POST['action']:
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in TOrders.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.billno)})
                request._set_post(post)
        return super(TOrdersAdmin, self).changelist_view(request, extra_context)


@admin.register(TRounds)
class TRoundAdmin(admin.ModelAdmin):
    """游戏局记录管理
    """

    def mybegintime(self,obj):
        if not obj.begintime:
            return obj.begintime
        else:
            return obj.begintime.strftime('%Y-%m-%d %H:%M:%S')
    mybegintime.short_description = u'开始时间'
    mybegintime.admin_order_field = 'begintime'

    def myclosetime(self,obj):
        if not obj.closetime:
            return obj.closetime
        else:
            return obj.closetime.strftime('%Y-%m-%d %H:%M:%S')
    myclosetime.short_description = u'结束时间'
    myclosetime.admin_order_field = 'closetime'


    list_display = ('roundcode','gametype','flag','videoid','dealer','cards','cardnum','pair','bankerpoint','playerpoint','mybegintime','myclosetime','shoecode')
    search_fields = ('roundcode','gametype','flag','dealer','cards','shoecode')
    list_filter = ('gametype','dealer','videoid','flag','cards','begintime','closetime')
    ordering = ('-roundcode',)
    readonly_fields = ('roundcode','gametype','flag','videoid','dealer','cards','cardnum','pair','bankerpoint','playerpoint','begintime','closetime','shoecode',)
    list_editable =  ('cards',)


    def recalcRound(self, request, queryset):

        head = u"重新结算局"
        command = 50016
        try:
            if len(queryset) == 1:
                roundcode = queryset[0].roundcode
                flag = queryset[0].flag
                if flag == 0:
                    response=requests.get('http://%s:%s/round?command=%s&roundcode=%s'%(url,port,command,roundcode))
                    if response.content == '60016':
                        message = u'结算成功'
                    else:
                         message = u'结算失败'
                    self.message_user(request, "%s: %s%s" %(head,roundcode,message))
                    super(TRoundAdmin,self).log_change(request, queryset[0], u'重新结算局:%s'%message) #自定义修改动作记录到log中
                else:
                    message = u'已经结算过,无法重新结算'
                    self.message_user(request, "%s: %s%s" %(head,roundcode,message))
            else:
                message = u'只能选择一局结算'
                self.message_user(request, "%s: %s" %(head,message))
        except Exception, e:
            message = u'发送指令出错'
            self.message_user(request, "%s: %s" %(head,message))
            super(TRoundAdmin,self).log_change(request, queryset[0], u'重新结算局:%s'%message) #自定义修改动作记录到log中
    recalcRound.short_description = u'重新结算局'

    def cancelRound(self, request, queryset):

        head = u"取消局注单结算"
        command = 50017
        try:
            if len(queryset) == 1:
                roundcode = queryset[0].roundcode
                flag = queryset[0].flag
                if flag == 0:
                    response=requests.get('http://%s:%s/round?command=%s&roundcode=%s'%(url,port,command,roundcode))
                    if response.content == '60017':
                        message = u'取消成功'
                    else:
                        message = u'取消失败'
                    self.message_user(request, "%s: %s%s" %(head,roundcode,message))
                    super(TRoundAdmin,self).log_change(request, queryset[0], u'取消局注单结算:%s'%message) #自定义修改动作记录到log中
                else:
                    message = u'已经结算过,无法取消'
                    self.message_user(request, "%s: %s%s" %(head,roundcode,message))
            else:
                message = u'只能取消一局'
                self.message_user(request, "%s: %s" %(head,message))
        except Exception, e:
            message = u'发送指令出错'
            self.message_user(request, "%s:%s" %(head,message))
            super(TRoundAdmin,self).log_change(request, queryset[0], u'取消局注单结算:%s'%message) #自定义修改动作记录到log中
    cancelRound.short_description = u'取消局注单结算'

    #def has_add_permission(self, request,obj=None):
    #    return False

    #def has_delete_permission(self,request,obj=None):
    #    return False

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

    actions = [recalcRound,cancelRound,setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]

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


@admin.register(TRecalcRounds)
class TRecalcRoundsAdmin(admin.ModelAdmin):
    """重新结算游戏局记录
    """
    def mycreate_time(self,obj):
        if not obj.create_time:
            return obj.create_time
        else:
            return obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
    mycreate_time.short_description = u'创建时间'
    mycreate_time.admin_order_field = 'create_time'

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

    actions = [setListPerPage_30,setListPerPage_50,setListPerPage_100,setListPerPage_300,setListPerPage_1000]

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
