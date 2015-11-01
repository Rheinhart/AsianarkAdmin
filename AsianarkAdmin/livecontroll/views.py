#coding:utf8
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    response = HttpResponseRedirect("/admin")
    return response
