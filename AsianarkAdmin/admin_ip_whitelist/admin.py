# -*- coding: utf-8 -*-
from django.contrib import admin

from AsianarkAdmin.admin_ext.pagination import FastPaginationMixin
from AsianarkAdmin.admin_ext.site import admin_site

from .models import DjangoAdminAccessIPWhitelist


@admin.register(DjangoAdminAccessIPWhitelist, site=admin_site)
class DjangoAdminAccessIPWhitelistAdmin(FastPaginationMixin, admin.ModelAdmin):
    list_display = ("ip", "whitelist_reason")
    search_fields = ("ip", "whitelist_reason")
    list_per_page = 50
