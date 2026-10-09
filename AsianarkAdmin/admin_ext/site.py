"""自定义 AdminSite：品牌化标题、首页看板、应用/模型排序。

老项目里 `class AsianarkAdminSite(admin.AdminSite)` 只是在类体里改了 `admin.site.*`，
换站点实例那行也没生效；模型排序靠 `tools/SortRegistryModelName.py` 猴补丁
（依赖 `admin.site._registry` 和 `context_data['app_list']` 私有结构，Django 3.1 起就炸了）。
这里用官方扩展点 `get_app_list()` / `index()` 重写。
"""
from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.urls import reverse

from . import dashboard


class AsianarkAdminSite(admin.AdminSite):
    site_header = "Asianark 赌场运营后台"
    site_title = "Asianark"
    index_title = "运营总览"
    enable_sidebar = True

    # 应用与模型的显示顺序（原来靠猴补丁按注册顺序排，这里显式声明）
    # 注意：LogEntry 属于 django.contrib.admin（app_label="admin"），admin_log 这个 app 里没有模型
    app_order = ["baccarat_Controll", "userinfo", "admin", "auth", "admin_ip_whitelist"]
    model_order = {
        "baccarat_Controll": [
            "torders",
            "trounds",
            "trecalcrounds",
            "ttable",
            "tvideo",
            "ttablelimitset",
            "tpersonallimitset",
            "tbulletin",
        ],
        "userinfo": ["tcustomers", "tcustomertrans", "tagents"],
    }
    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label=app_label)
        app_rank = {label: index for index, label in enumerate(self.app_order)}
        app_list.sort(key=lambda app: app_rank.get(app["app_label"], len(app_rank)))
        for app in app_list:
            model_rank = {name: index for index, name in enumerate(self.model_order.get(app["app_label"], []))}
            # 注意：app_list 里的 model 字典没有 "model_name" 键，只有 object_name
            app["models"].sort(key=lambda model: model_rank.get(model["object_name"].lower(), len(model_rank)))
        return app_list

    def index(self, request, extra_context=None):
        extra_context = dict(extra_context or {})
        extra_context["kpi"] = dashboard.kpi_stats(refresh=bool(request.GET.get("refresh")))
        extra_context["quick_links"] = [
            {"label": "未结算的局", "url": reverse("admin:baccarat_Controll_trounds_changelist") + "?flag__exact=0"},
            {"label": "今日注单", "url": reverse("admin:baccarat_Controll_torders_changelist") + "?date_range=1d"},
            {"label": "近 7 天注单", "url": reverse("admin:baccarat_Controll_torders_changelist") + "?date_range=7d"},
            {"label": "后台操作日志", "url": reverse("admin:admin_logentry_changelist")},
        ]
        return super().index(request, extra_context)


admin_site = AsianarkAdminSite()

# 复用 Django 自带的用户/权限组后台
admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)
