"""测试运行器。

这个项目的 settings 包（``AsianarkAdmin``）直接放在仓库根目录下，
unittest 的自动发现会把根目录当成一个多余的子模块去找
（``manage.py test`` 不带参数时会报 ``No module named 'AsianarkAdmin.AsianarkAdmin'``）。
这里把默认 label 定成项目包，其它参数（``manage.py test AsianarkAdmin.baccarat_Controll``、
``--keepdb``、``-v 2`` 等）都照原样可用。
"""

from __future__ import annotations

import os

from django.test.runner import DiscoverRunner as DjangoDiscoverRunner


class DiscoverRunner(DjangoDiscoverRunner):
    def build_suite(self, test_labels=None, **kwargs):
        # 仓库根目录就是 sys.path 的顶层，不告诉 unittest 的话它会去项目包里
        # 再找一个同名的子模块（AsianarkAdmin.AsianarkAdmin）。
        if self.top_level is None:
            self.top_level = os.getcwd()
        return super().build_suite(test_labels or ["AsianarkAdmin"], **kwargs)
