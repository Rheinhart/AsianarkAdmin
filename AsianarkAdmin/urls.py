"""URL 配置。

老写法有两个坑，这里都修掉了：
* `class AsianarkAdminSite(admin.AdminSite)` 的类体里只是在改 `admin.site.*`，
  而 `admin.admin_site = AsianarkAdminSite()` 对 `@admin.register` 用的 `admin.site`
  完全不起作用 —— 整个类是空操作。现在用真正的自定义站点实例挂到 /admin/。
* `url(r'^admin/', ...)` 没有 `$`，会匹配所有以 admin 开头的路径。现在用 path()。
"""
from django.urls import path

from AsianarkAdmin.admin_ext.site import admin_site
from AsianarkAdmin.baccarat_Controll import views

urlpatterns = [
    path("admin/", admin_site.urls),
    path("", views.index, name="index"),
]
