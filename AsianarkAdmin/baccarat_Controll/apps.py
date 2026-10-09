# -*- coding: utf-8 -*-
from django.apps import AppConfig


class BaccaratControllConfig(AppConfig):
    # label 保持与老项目一致（baccarat_Controll），模板路径与 admin URL 名不变
    name = "AsianarkAdmin.baccarat_Controll"
    label = "baccarat_Controll"
    verbose_name = "游戏控制"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from . import signals  # noqa: F401  注册模型信号
