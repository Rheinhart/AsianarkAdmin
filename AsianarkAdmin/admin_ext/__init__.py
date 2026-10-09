"""可复用的后台扩展工具包（无模型，只提供 AdminSite / ModelAdmin 能力）。

对应老项目里散落在 9 个 ModelAdmin 中的重复代码：

| 老写法 | 这里 |
| --- | --- |
| 45 个 `setListPerPage_*` + 9 处 `request._set_post` hack | `pagination.FastPaginationMixin`（`?per_page=` GET 参数） |
| `list_filter=('create_time',)`（对全表 DISTINCT） | `filters.RelativeDateFilter` |
| `changelist_view` 里手写全表 sum | `stats.ChangelistStatsMixin` |
| `mycreate_time` 手写 strftime × 十几个 | `badges.dt`（走 settings 的 DATETIME_FORMAT） |
| `del actions['delete_selected']` | 用 `has_delete_permission`，admin 自己会过滤 |
| `tools/SortRegistryModelName.py` 猴补丁 | `site.AsianarkAdminSite.get_app_list` |
"""

# AppConfig 由 Django 自动发现（apps.py 里唯一的 AppConfig 子类）。
