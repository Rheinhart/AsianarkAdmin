#coding:utf8
'''
Created on 2015-10-13

@author: Thomas
'''

from AsianarkAdmin.adminuser.models import TControllers
from django.shortcuts import render_to_response,HttpResponseRedirect
from AsianarkAdmin.errormsg import *

def login_no_user(request):

    '''没有用户的登陆情况
    '''
    return render_to_response('login.html',{'errormsg':''})

def login_check_user(request):
    '''验证用户
    '''
    username = request.POST['username']
    password = request.POST['password']
    try:
        theuser = TControllers.objects.get(loginname=username)
    except Exception:
        theuser = None
    if not theuser:
        return render_to_response('login.html',{'errormsg':USER_ERROR})
    if not theuser.check_password(password):
        return render_to_response('login.html',{'errormsg':PASSWORD_ERROR})
    response = HttpResponseRedirect("/main")
    response.set_cookie('login_user', username,max_age=600)
    return render_to_response('main.html')

