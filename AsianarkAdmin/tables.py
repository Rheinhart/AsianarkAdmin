# -*- coding: utf-8 -*-
"""业务表清单。

所有业务模型都是 `managed=False`（表结构属于线上老库），所以 Django 的 migrate
和测试库都不会自动建这些表。这里集中列出，供两处使用：
* `manage.py init_local_db`：在本地 sqlite 里建同样的表；
* 测试：`admin_ext.test_utils.ensure_business_tables()`。
"""
from __future__ import annotations


def business_models() -> list:
    from AsianarkAdmin.baccarat_Controll.models import (
        TBulletin,
        TOrders,
        TPersonalLimitset,
        TRecalcRounds,
        TRounds,
        TTable,
        TTableLimitset,
        TVideo,
    )
    from AsianarkAdmin.userinfo.models import TAgents, TCustomerTrans, TCustomers

    # 顺序 = 依赖顺序（先建被引用的表）
    return [
        TBulletin,
        TVideo,
        TTableLimitset,
        TPersonalLimitset,
        TTable,
        TRounds,
        TOrders,
        TRecalcRounds,
        TCustomers,
        TCustomerTrans,
        TAgents,
    ]
