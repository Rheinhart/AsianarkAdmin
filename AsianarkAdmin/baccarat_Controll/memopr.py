#coding:utf8
"""
@__author__ = 'Thomas'
"""
from AsianarkAdmin.tools.fireflymem.dbpool import dbpool
from AsianarkAdmin.tools.fireflymem.memclient import mclient
from AsianarkAdmin.tools.fireflymem.mmode import MAdmin
from AsianarkAdmin.tools.fireflymem.madminanager import MAdminManager
from AsianarkAdmin.settings import CACHES,DATABASES


class Memmode_Operation:
    """Video, Table的缓存操作, 借助firefly memecache的相关api
    """

    def __init__(self):
        """set the mamcache and database """


        self.host = [DATABASES['default'].get('HOST')][0]
        self.user = [DATABASES['default'].get('USER')][0]
        self.password = [DATABASES['default'].get('PASSWORD')][0]
        self.port = int([DATABASES['default'].get('PORT')][0])
        self.dbname = [DATABASES['default'].get('NAME')][0]
        self.charset = "utf8"
        dbpool.initPool(host = self.host, user = self.user, passwd = self.password,
                    port = self.port, db = self.dbname, charset = self.charset)

        self.address = [CACHES['default'].get('LOCATION')]
        self.hostname = [CACHES['default'].get('HOSTNAME')][0]
        mclient.connect(self.address,self.hostname)

        self.tb_video_admin = MAdmin('t_video', 'videoid', fk="flag")
        MAdminManager().registe(self.tb_video_admin)
        self.tb_table_admin = MAdmin('t_table', 'tableid', fk='videoid')
        MAdminManager().registe(self.tb_table_admin)

    def syncVideoMemAndDb(self):
        """同步视频缓数据库
        Sync Viedeoinfo from Memcache into database!
        """
        obj = self.tb_video_admin.getAllPkByFk(0)
        for id in obj:
            print self.tb_video_admin.getObjData(id)
        obj = self.tb_video_admin.getAllPkByFk(1)
        for id in obj:
            print self.tb_video_admin.getObjData(id)
        self.tb_video_admin.checkAll()
        #MAdminManager().checkAdmins()

    def changeVideoInMem(self,mdata):
        """修改视频缓存
        """
        mmode = self.tb_video_admin.getObj(mdata['videoid'])
        if mmode:
            mmode.update_multi(mdata)
        else:
            print 'Not found in memcached!'

    #def refreshVideoDbtoMem(self):
    #    """更新数据库到视频缓存
    #    """
    #    pass
        #obj = self.tb_video_admin.getAllPkByFk(0)
        #for id in obj:
        #    print self.tb_video_admin.getObjData(id)
        #print '*'*20

        #self.tb_video_admin.insert()
        # #obj = self.tb_video_admin.getAllPkByFk(0)
        # for id in obj:
        #     print self.tb_video_admin.getObjData(id)
        # obj = self.tb_video_admin.getAllPkByFk(1)
        # for id in obj:
        #     print self.tb_video_admin.getObjData(id)

    def syncTableMemAndDb(self):
        """同步桌台缓存数据库
        Sync Tableinfo from Memcache into database!
        """
        print 'Show after sync'
        obj = self.tb_table_admin.getAllPkByFk(0)
        for id in obj:
            print self.tb_table_admin.getObjData(id)
        self.tb_table_admin.checkAll()

    def changeTableInMem(self,mdata):
        """修改桌台缓存
        """
        mmode = self.tb_table_admin.getObj(mdata['tableid'])
        if mmode:
            mmode.update_multi(mdata)
        else:
            print 'Not found in memcached!'

memopr=Memmode_Operation() #链接memcache和database

