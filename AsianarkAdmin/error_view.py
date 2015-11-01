#coding:utf8
'''
Created on 2013-1-4

@author: lan (www.9miao.com)
'''
#from django.http import HttpResponse
from django.shortcuts import render_to_response

def Error_404(request):
    return render_to_response("404.html")
    
def Error_500(request):
    return render_to_response("404.html")
