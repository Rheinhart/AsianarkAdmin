#coding:utf8
"""
@__author__ = 'Thomas'
"""
from BaccaratAdmin.tools.fireflymem.dbpool import dbpool
from BaccaratAdmin.tools.fireflymem.memclient import mclient
from BaccaratAdmin.tools.fireflymem.mmode import MAdmin
from BaccaratAdmin.tools.fireflymem.madminanager import MAdminManager
from datetime import datetime


if __name__ == '__main__':

    hostname = '127.0.0.1'
    user = 'root'
    password = '123456'
    #hostname = '183.91.54.138'
    #user = 'web'
    #password = 'web.ak'
    port = 3306
    dbname = 'bjl'
    charset = "utf8"
    dbpool.initPool(host = hostname, user = user, passwd = password,
                    port = port, db = dbname, charset = charset)
    address = ['127.0.0.1:11211']
    hostname = 'localhost'
    mclient.connect(address, hostname)

    tb_video_admin = MAdmin('t_video', 'videoid', fk="flag")
    tb_video_admin.insert()
    MAdminManager().registe(tb_video_admin)
    obj = tb_video_admin.getAllPkByFk(0)
    for id in obj:
        print tb_video_admin.getObjData(id)
    obj = tb_video_admin.getAllPkByFk(1)
    for id in obj:
        print tb_video_admin.getObjData(id)


