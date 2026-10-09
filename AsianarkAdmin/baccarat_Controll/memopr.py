# -*- coding: utf-8 -*-
"""t_video / t_table 的 memcache 内存模型同步（firefly 那套）。

老代码在模块底部写了 `memopr = Memmode_Operation()` —— 于是 **导入 models.py 就会去连
MySQL 和 memcached**（`models.py` 里 `from memopr import memopr`），任何 `manage.py`
命令、跑测试都需要外部服务在线。现在改成懒加载 + 可用 `ASIANARK_MEMCACHE_ENABLED=0` 关掉。
"""
from __future__ import annotations

import logging

from django.conf import settings

logger = logging.getLogger("asianark.memopr")


class MemmodeOperation:
    """借助 fireflymem 的 API 同步视频/桌台的内存模型。"""

    def __init__(self):
        from AsianarkAdmin.tools.fireflymem.dbpool import dbpool
        from AsianarkAdmin.tools.fireflymem.memclient import mclient
        from AsianarkAdmin.tools.fireflymem.mmode import MAdmin
        from AsianarkAdmin.tools.fireflymem.madminanager import MAdminManager

        db = settings.DATABASES["default"]
        dbpool.initPool(
            host=db.get("HOST") or "127.0.0.1",
            user=db.get("USER", ""),
            passwd=db.get("PASSWORD", ""),
            port=int(db.get("PORT") or 3306),
            db=db.get("NAME", ""),
            charset="utf8mb4",
        )

        mem = settings.MEMCACHE
        mclient.connect([mem["LOCATION"]], mem["HOSTNAME"])

        self.tb_video_admin = MAdmin("t_video", "videoid", fk="flag")
        MAdminManager().registe(self.tb_video_admin)
        self.tb_table_admin = MAdmin("t_table", "tableid", fk="videoid")
        MAdminManager().registe(self.tb_table_admin)

    # ------------------------------------------------------------------ 同步
    def syncVideoMemAndDb(self):
        """同步视频缓存。注意：数据库与缓存不一致时，被标记删除的值会复现。"""
        self.tb_video_admin.checkAll()

    def syncTableMemAndDb(self):
        """同步桌台缓存。"""
        self.tb_table_admin.checkAll()

    # ------------------------------------------------------------------ 单条修改
    def changeVideoInMem(self, mdata):
        mmode = self.tb_video_admin.getObj(mdata["videoid"])
        if mmode:
            mmode.update_multi(mdata)
        else:
            logger.warning("memcache 中找不到视频 %s", mdata.get("videoid"))

    def changeTableInMem(self, mdata):
        mmode = self.tb_table_admin.getObj(mdata["tableid"])
        if mmode:
            mmode.update_multi(mdata)
        else:
            logger.warning("memcache 中找不到桌台 %s", mdata.get("tableid"))


_instance = None


def get_memopr() -> MemmodeOperation:
    """懒加载单例。缺依赖 / 连不上时抛 RuntimeError，由调用方（services）兜住。"""
    global _instance
    if _instance is None:
        try:
            _instance = MemmodeOperation()
        except Exception as exc:  # pragma: no cover - 需要 MySQLdb/memcache 依赖
            raise RuntimeError(f"memcache 集成不可用: {exc}") from exc
    return _instance
