"""按代理（agentcode）做数据隔离。

老代码只在客户表上做了隔离，而且写法是 `qs.filter(agentcode=inner_qs)`
（把一个 QuerySet 当值传进去，多行就报错），注单和流水完全没有隔离。
现在统一成 mixin，所有带 agentcode 的表都用同一套规则。
"""
from __future__ import annotations

import logging

logger = logging.getLogger("asianark.scoping")


class AgentScopedAdminMixin:
    """非超管只能看到自己代理名下的数据。"""

    agent_field = "agentcode"

    def scoped_agent_codes(self, request) -> list[int] | None:
        """返回当前后台账号绑定的代理 code；超管返回 None 表示不限制。"""
        from AsianarkAdmin.userinfo.models import TAgents

        if request.user.is_superuser:
            return None
        return list(TAgents.objects.filter(user=request.user).values_list("agentcode", flat=True))

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        codes = self.scoped_agent_codes(request)
        if codes is None:
            return queryset
        return queryset.filter(**{f"{self.agent_field}__in": codes})

    def get_search_fields(self, request):
        """非超管不能按 agentcode 搜（否则会看到别人名下的数据）。"""
        fields = list(super().get_search_fields(request) or ())
        if self.scoped_agent_codes(request) is not None:
            fields = [f for f in fields if self.agent_field not in f]
        return fields
