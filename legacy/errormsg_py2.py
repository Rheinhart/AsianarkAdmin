#coding:utf8
'''
Created on 2012-12-29
错误消息
@author: lan (www.9miao.com)
'''
NO_USER_OR_PASSWORD = u'<font color="#FF0000">用户名或密码不能为空</font>'
PASSWORD_ERROR = u'<font color="#FF0000">两次密码不一致</font>'
USER_ERROR = u'用户名不存在'
USER_EXITS = u'用户名已存在'
PASSWORD_ERROR = u'密码错误'
NO_MONEY = u'您的余额不足'
MUST_LOGIN = u'请先登陆'
APPLY_SUCCESS = u'提交成功'
POST_ERROR = u'<font color="#00FF00">信息不全</font>'

#错误代号
LOCAL_ARGS_ERROR = '-21'#GI部分接收参数错误
LOCAL_MD5_ERROR  = '-20'#GI部分MD5校验失败
LOCAL_EXCEPTION  = '-22'#GI部分内部异常
LOCAL_REPEATED_ORDER = '-29'#GI部分重复订单号
SUCCESS = '1'#操作成功
GAME_MD5_ERROR = '0'#游戏服务器MD5验证不通过
GAME_NO_USER = '-1'#游戏中角色信息不存在
GAME_DB_ERROR = '-10'#游戏服务器中数据库写入失败
GAME_REPEATED_ORDER = '-9'#游戏服务器中检测到相同的订单号


