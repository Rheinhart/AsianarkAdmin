#coding:utf8
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    response = HttpResponseRedirect("/admin")
    return response

def sendClientAdr(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    response = HttpResponseRedirect("/admin/TVideos/add")
    return response