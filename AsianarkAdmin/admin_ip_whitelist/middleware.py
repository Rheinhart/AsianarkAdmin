# -*- coding: utf-8 -*-
"""后台访问 IP 白名单中间件。

老实现有两个问题：
1. 类里写的是 `process_request`（Django 1.4 风格），1.10 之后必须继承 `MiddlewareMixin`
   或写成新式中间件，否则请求根本不会被拦；
2. 白名单在 `__init__` 里一次性读进内存，之后新增/删除白名单不生效，
   而 settings 里的开关拼成了 `ADMIN_ACCEES_WHITELIST_ENABLED`（少个 S），
   中间件读的是 `ADMIN_ACCESS_WHITELIST_ENABLED` → 默认值 True，一启用就全量拦截。
"""
from __future__ import annotations

import logging

from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("asianark.ipwhitelist")


class AdminAccessIPWhiteListMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.enabled = getattr(settings, "ADMIN_ACCESS_WHITELIST_ENABLED", True)
        self.message = getattr(settings, "ADMIN_ACCESS_WHITELIST_MESSAGE", "Your ip address is not allowed!")
        self.use_x_forwarded_for = getattr(settings, "ADMIN_ACCESS_WHITELIST_USE_X_FORWARDED_FOR", False)

    def __call__(self, request):
        if not self.enabled or not request.path.startswith("/admin"):
            return self.get_response(request)

        ip = self._client_ip(request)
        if self._is_whitelisted(ip):
            return self.get_response(request)

        logger.info("拒绝 %s 访问 %s", ip, request.path)
        return HttpResponseForbidden(f"{self.message}\n<!-- {ip} -->", content_type="text/html")

    def _client_ip(self, request) -> str:
        if self.use_x_forwarded_for:
            forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
            if forwarded:
                return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")

    @staticmethod
    def _is_whitelisted(ip: str) -> bool:
        from .models import is_ip_whitelisted

        return is_ip_whitelisted(ip)
