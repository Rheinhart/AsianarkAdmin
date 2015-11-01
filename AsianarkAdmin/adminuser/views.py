#coding:utf8

# Create your views here.
from django.shortcuts import render_to_response,HttpResponseRedirect,HttpResponse
from AsianarkAdmin.toolfunc import checklogin,checkSecurity
import admin
import datetime

#@checkSecurity
def login(request):
    '''用户登录页面'''
    if request.method == "POST":
        return admin.login_check_user(request)
    else:
        return admin.login_no_user(request)

#@checkSecurity
@checklogin
def main(request):
    username = request.COOKIES.get("login_user")
    return render_to_response('main.html',{'username':username,
                                           'nowdate':datetime.date.today()})

#@checkSecurit
@checklogin
def loginout(request):
    '''注销
    '''
    response = HttpResponseRedirect("/login")
    response.delete_cookie('login_user')
    return response
