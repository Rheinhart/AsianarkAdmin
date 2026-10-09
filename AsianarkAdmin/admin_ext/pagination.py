"""列表页分页：每页条数按请求切换 + 大表不做精确 COUNT。

老实现的问题（见 review）：
1. `admin.ModelAdmin.list_per_page = N` 改的是**基类属性** → 进程级、跨用户、永不复位，
   多 worker 部署下每个 worker 各改各的，翻页结果不确定。
2. 用 action 实现"页面设置" → 必须勾选行 → 只能 `for u in Model.objects.all(): post.update(...)`
   伪造勾选（O(N) + 撞 DATA_UPLOAD_MAX_NUMBER_FIELDS）。
3. 状态不在 URL 里 → 页码漂移、不能分享、重启丢失。
4. 默认 `show_full_result_count=True` → 每次翻页两次全表 COUNT。

这里改成框架的扩展点：`?per_page=` GET 参数 + `get_paginator()` + `get_changelist()`，
写一次，所有 ModelAdmin 一行接入。
"""
from __future__ import annotations

from django.contrib.admin.views.main import ChangeList
from django.core.paginator import EmptyPage, Page, Paginator


class FastChangeList(ChangeList):
    """把分页用的查询参数从"模型查找参数"里排除。

    不排掉的话 `?per_page=50` 会被 ChangeList 当成 `filter(per_page=50)`，
    抛 FieldError → IncorrectLookupParameters → 页面报"错误的查找参数"并跳回首页。
    """

    EXTRA_PARAMS = ("per_page", "fullcount")

    def get_filters_params(self, params=None):
        lookup_params = super().get_filters_params(params)
        for name in self.EXTRA_PARAMS:
            lookup_params.pop(name, None)
        return lookup_params


class CursorPage(Page):
    """估算模式下"有没有下一页"由"这一页取满没有"决定，而不是由总页数决定。"""

    def has_next(self):
        if getattr(self.paginator, "estimated", False):
            return len(self.object_list) >= self.paginator.per_page
        return super().has_next()


class FastPaginator(Paginator):
    """小结果集给精确计数；超过 probe_rows 就不 COUNT，改用游标式翻页。"""

    probe_rows = 5000
    estimated = False

    def __init__(self, *args, probe_rows=None, **kwargs):
        super().__init__(*args, **kwargs)
        if probe_rows is not None:
            self.probe_rows = int(probe_rows)
        self._count = None
        self.fetched_has_next = False

    # ---------------- 计数 ----------------
    @property
    def count(self):
        if self._count is None:
            if self.probe_rows <= 0:  # ?fullcount=1 → 用户要精确值
                self._count = self.object_list.count()
            else:
                probe = list(self.object_list.values_list("pk", flat=True)[: self.probe_rows + 1])
                if len(probe) <= self.probe_rows:
                    self._count = len(probe)
                else:
                    self.estimated = True
                    self._count = self.probe_rows + 1
        return self._count

    # ---------------- 取页 ----------------
    def validate_number(self, number):
        # 估算模式下不预设页数上限，有没有下一页交给实际取数
        cap = 10**9 if self.estimated else self.num_pages
        return self._validate_number(number, cap)

    def page(self, number):
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        # 估算模式下 self.count 是假的，不能用它截断切片
        if not self.estimated and top + self.orphans >= self.count:
            top = self.count
        page = self._get_page(self.object_list[bottom:top], number, self)
        if not page.object_list and number > 1:
            raise EmptyPage(self.error_messages["no_results"])
        self.fetched_has_next = len(page.object_list) >= self.per_page
        return page

    def _get_page(self, *args, **kwargs):
        return CursorPage(*args, **kwargs)

    # ---------------- 页码窗口 ----------------
    def get_elided_page_range(self, number=1, *, on_each_side=3, on_ends=2):
        if not self.estimated:
            yield from super().get_elided_page_range(
                number, on_each_side=on_each_side, on_ends=on_ends
            )
            return
        # 尾部页数未知：只给"当前页附近"，靠"下一页 →"继续翻，不编造 .. 末页
        number = self.validate_number(number)
        start = max(1, number - on_each_side)
        if start > 1:
            yield 1
            yield self.ELLIPSIS
        yield from range(start, number + on_each_side + 1)


class FastPaginationMixin:
    """用法：``class XxxAdmin(FastPaginationMixin, admin.ModelAdmin)``"""

    count_probe_rows = 5000
    per_page_options = (25, 50, 100, 200)
    default_per_page = 50
    # 大表不需要"未筛选的总数"，省掉一次全表 COUNT
    show_full_result_count = False

    def _resolve_per_page(self, request) -> int:
        try:
            value = int(request.GET.get("per_page"))
        except (TypeError, ValueError):
            return self.default_per_page
        return value if value in self.per_page_options else self.default_per_page

    def changelist_view(self, request, extra_context=None):
        per_page = self._resolve_per_page(request)
        # ModelAdmin 实例在进程里是单例，直接赋值就又变成"全局状态"。
        # 必须请求内临时改、finally 复位 —— 这才是按请求隔离。
        saved, self.list_per_page = self.list_per_page, per_page
        try:
            response = super().changelist_view(request, extra_context=extra_context)
        finally:
            self.list_per_page = saved
        cl = getattr(response, "context_data", {}).get("cl")
        if cl is not None:
            # 分页条需要这两个值；{% pagination cl %} 只把 cl 传进模板，所以挂在 cl 上
            cl.per_page_options = self.per_page_options
            cl.current_per_page = per_page
        return response

    def get_changelist(self, request, **kwargs):
        return FastChangeList

    def get_paginator(self, request, queryset, per_page, orphans=0, allow_empty_first_page=True):
        probe = 0 if request.GET.get("fullcount") else self.count_probe_rows
        return FastPaginator(
            queryset,
            per_page,
            orphans=orphans,
            allow_empty_first_page=allow_empty_first_page,
            probe_rows=probe,
        )
