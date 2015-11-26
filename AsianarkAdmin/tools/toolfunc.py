#coding:utf8
'''
Created on 2012-12-29

@author: lan (www.9miao.com)
'''
from django.shortcuts import HttpResponseRedirect,render_to_response
#from AsianarkAdmin.serverinfo.models import WhiteList
import hashlib,socket

def checklogin(func):
    '''检测是否登录
    '''
    def _(*args,**kw):
        username = args[0].COOKIES.get("login_user")
        if not username:
            return HttpResponseRedirect('/login')
        return func(*args,**kw)
    return _

def checkSecurity(func):
    """安全性检测
    """
    def _(*args,**kw):
        clientIp = args[0].META['REMOTE_ADDR']
        try:
            white = WhiteList.objects.get(ip=clientIp)
        except:
            white = None
        if not white:
            return render_to_response('security_error.html')
        return func(*args,**kw)
    return _

def checkMD5(*args):
    '''检测MD5是否正确'''
    return True
    import urllib
    values = args[:-2]
    sign = args[-2]
    privatekey = args[-1]
    md_first = hashlib.md5()
    md_first.update(privatekey)
    key_last = md_first.hexdigest().upper()
    value_str = ''.join(values)
    value_str=urllib.quote(value_str)
    md_value = hashlib.md5()
    md_value.update(value_str)
    md_value_md5 = md_value.hexdigest().upper()
    mingwenzifu = key_last+md_value_md5
    md_last = hashlib.md5()
    md_last.update(mingwenzifu)
    sign_now = md_last.hexdigest().upper()
    if sign!=sign_now:
        return False
    else:
        return True

def MakeMD5(args,privatekey):
    """生成MD5
    """
    import urllib
    md_first = hashlib.md5()
    md_first.update(privatekey)
    key_last = md_first.hexdigest().upper()
    value_str = ''.join(args)
    value_str=urllib.quote(value_str)
    md_value = hashlib.md5()
    md_value.update(value_str)
    md_value_md5 = md_value.hexdigest().upper()
    mingwenzifu = key_last+md_value_md5
    md_last = hashlib.md5()
    md_last.update(mingwenzifu)
    sign_now = md_last.hexdigest().upper()
    return sign_now

def MakeSecurityURL(address,port,call,serverkey,argsdir):
    """生成安全连接
    """
    args = [item[1] for item in argsdir]
    sign_now = MakeMD5(args,serverkey)
    argsstr = ['%s=%s&'%item for item in argsdir]
    argsstr.append("sign=%s"%sign_now)
    urls = "http://%s:%s/%s?"%(address,port,call)
    urls += ''.join(argsstr)
    return urls

def MakeLoginArgs(serverkey,argsdir):
    """生成安全登陆参数
    """
    args = [item[1] for item in argsdir]
    sign_now = MakeMD5(args,serverkey)
    argsstr = ['%s=%s&'%item for item in argsdir]
    argsstr.append("sign=%s"%sign_now)
    sec_args = ''.join(argsstr)
    return sec_args

NORMAL=0
ERROR=1
TIMEOUT=5

def ping(ip,port,timeout=TIMEOUT):
    try:
        cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        address=(str(ip),int(port))
        status = cs.connect_ex((address))
        cs.settimeout(timeout)
        if status != NORMAL :
            return False
        else:
            return True
    except:
        return ERROR

    return True


