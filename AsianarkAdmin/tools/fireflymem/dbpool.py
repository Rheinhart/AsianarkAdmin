#coding:utf8
'''
Created on 2013-5-8

@author: lan (www.9miao.com)
'''
try:  # DBUtils 3.x
    from dbutils.pooled_db import PooledDB
except ImportError:  # DBUtils 1.x
    from DBUtils.PooledDB import PooledDB

try:
    import MySQLdb
    DBCS = {'mysql': MySQLdb}
except ImportError:  # pragma: no cover
    import pymysql
    DBCS = {'mysql': pymysql}

class DBPool(object):
    '''
    '''
    def initPool(self,**kw):
        '''
        '''
        self.config = kw
        creator = DBCS.get(kw.get('engine','mysql'),MySQLdb)
        self.pool = PooledDB(creator,5,**kw)
        
    def connection(self):
        return self.pool.connection()

dbpool = DBPool()

