# -*- coding: utf-8 -*-
"""后台登录 IP 白名单。"""
from __future__ import annotations

from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

CACHE_PREFIX = "DJANGO_ADMIN_ACCESS_WHITELIST:"
NEGATIVE_TTL = 300


class DjangoAdminAccessIPWhitelist(models.Model):
    whitelist_reason = models.CharField(max_length=255, verbose_name="白名单", help_text="填写加白名单的原因")
    ip = models.CharField(max_length=255, help_text="白名单 IP")

    class Meta:
        permissions = [("can_whitelist_user", "Can Whitelist User")]
        verbose_name = "管理员登录IP白名单"
        verbose_name_plural = "管理员登录IP白名单"
        db_table = "django_admin_access_ip_whitelist"

    def __str__(self):
        return f"白名单 {self.ip}（{self.whitelist_reason}）"


def _cache_key(ip: str) -> str:
    return CACHE_PREFIX + ip


def is_ip_whitelisted(ip: str) -> bool:
    """先查缓存，未命中回源数据库并缓存结果（老实现只在进程启动时读一次）。"""
    if cache.get(_cache_key(ip)):
        return True
    hit = DjangoAdminAccessIPWhitelist.objects.filter(ip=ip).exists()
    if hit:
        cache.set(_cache_key(ip), "1", None)
    else:
        cache.set(_cache_key(ip), "", NEGATIVE_TTL)
    return hit


@receiver(post_save, sender=DjangoAdminAccessIPWhitelist, dispatch_uid="ip_whitelist_cache_set")
def _update_cache(sender, instance, **kwargs):
    cache.set(_cache_key(instance.ip), "1", None)


@receiver(post_delete, sender=DjangoAdminAccessIPWhitelist, dispatch_uid="ip_whitelist_cache_del")
def _delete_cache(sender, instance, **kwargs):
    cache.delete(_cache_key(instance.ip))
