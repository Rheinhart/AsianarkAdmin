# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    """根路径直接进后台。"""
    return HttpResponseRedirect(reverse("admin:index"))
