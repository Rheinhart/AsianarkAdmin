#coding:utf8
"""
@__author__ = 'Thomas'
"""
from AsianarkAdmin.tools.fireflymem.dbpool import dbpool
from AsianarkAdmin.tools.fireflymem.memclient import mclient
from AsianarkAdmin.tools.fireflymem.mmode import MAdmin
from AsianarkAdmin.tools.fireflymem.madminanager import MAdminManager



if __name__ == '__main__':

    hostname = '183.91.54.138'
    user = 'web'
    password = 'web.ak'
    port = 3306
    dbname = 'bjl'
    charset = "utf8"
    dbpool.initPool(host = hostname, user = user, passwd = password,
                     port = port, db = dbname, charset = charset)
    address = ['127.0.0.1:11211']
    hostname = 'bjl'
    mclient.connect(address, hostname)
    tb_video = MAdmin('t_video', 'videoid', fk="flag")
    obj = tb_video.getAllPkByFk(0)
    for id in obj:
        print tb_video.getObjData(id)
    print '*'*20
    from AsianarkAdmin.baccarat_Controll.memopr import Memmode_Operation

    obj = tb_video.getAllPkByFk(0)
    for id in obj:
        print tb_video.getObjData(id)



