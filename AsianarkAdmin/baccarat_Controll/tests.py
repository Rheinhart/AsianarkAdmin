# -*- coding: utf-8 -*-
"""后台回归测试：分页、统计条、写路径、权限隔离、推送失败降级。

业务表是 managed=False，测试库不会自动建表，所以用
`admin_ext.test_utils.BusinessTablesTestCaseMixin` 先建表。
"""
from __future__ import annotations

from datetime import timedelta

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from AsianarkAdmin.admin_ext.site import admin_site
from AsianarkAdmin.admin_ext.test_utils import BusinessTablesTestCaseMixin
from AsianarkAdmin.baccarat_Controll import services
from AsianarkAdmin.baccarat_Controll.models import TOrders, TRounds, TVideo, TTable
from AsianarkAdmin.userinfo.models import TAgents, TCustomers


def make_superuser() -> User:
    user = User.objects.create_user("root", password="pw", is_staff=True, is_superuser=True)
    return user


def make_customer(loginname: str, agentcode: int = 1) -> TCustomers:
    return TCustomers.objects.create(
        loginname=loginname,
        agentcode=agentcode,
        password="x",
        nickname=loginname,
        credit_cents=0,
        limitid="A",
        create_ip="10.0.0.1",
    )


def make_orders(count: int, loginname: str = "p1", start: int = 1) -> None:
    now = timezone.now()
    TOrders.objects.bulk_create(
        [
            TOrders(
                billno=start + index,
                gametype="BJL",
                loginname=loginname,
                agentcode=1,
                roundcode=f"R{start + index:08d}",
                videoid="V001",
                tableid="T001",
                seat=0,
                dealer="d1",
                flag=1,
                playtype=0,
                bet_amount_cents=1000,
                valid_bet_amount_cents=1000,
                win_amount_cents=500,
                hashcode="",
                before_credit_cents=0,
                after_credit_cents=500,
                create_time=now - timedelta(hours=index),
                reckon_time=now,
                create_ip="10.0.0.1",
            )
            for index in range(count)
        ]
    )


def grant_agent_permissions(user: User) -> None:
    """给代理账号只开“查看”权限（修改只开自己名下的表）。

    老代码只靠 `get_queryset` 隔数据，没考虑 Django admin 本身的权限；
    没权限的账号进不了列表页（403），隔逻辑就无从生效。
    """
    user.user_permissions.add(
        *Permission.objects.filter(
            codename__in=[
                "view_tcustomers",
                "change_tcustomers",
                "view_tcustomertrans",
                "change_tcustomertrans",
                "view_torders",
                "change_torders",
            ]
        )
    )


class BaseAdminTest(BusinessTablesTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = make_superuser()

    def setUp(self):
        self.client.force_login(self.user)

    def url(self, name: str) -> str:
        return reverse(name)


# --------------------------------------------------------------------- 页面冒烟
class SmokeTests(BaseAdminTest):
    """所有注册过的列表页 + 首页都能渲染（app_label / 模板路径写错会在这里暴露）。"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        make_customer("p1")
        make_orders(5)

    def test_index_page(self):
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "今日注单")

    def test_every_registered_changelist_renders(self):
        for model in admin_site._registry:
            url = reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist")
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, url)

    def test_change_forms_render(self):
        video = TVideo.objects.create(videoid="V001", gametype="BJL", bettime=10, url="http://a")
        TTable.objects.create(tableid="T001", videoid=video, gametype="BJL", limitid="A", seats=7)
        for model in admin_site._registry:
            opts = model._meta
            instance = model.objects.first()
            if instance is None:
                continue
            url = reverse(f"admin:{opts.app_label}_{opts.model_name}_change", args=[instance.pk])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, url)


# --------------------------------------------------------------------- 分页
class PaginationTests(BaseAdminTest):
    changelist_url = reverse("admin:baccarat_Controll_torders_changelist")

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        make_customer("p1")
        make_orders(120)

    def pks_on_page(self, query: str) -> list[int]:
        response = self.client.get(f"{self.changelist_url}?{query}")
        self.assertEqual(response.status_code, 200)
        return [obj.pk for obj in response.context["cl"].result_list]

    def test_default_per_page_comes_from_modeladmin(self):
        response = self.client.get(self.changelist_url)
        self.assertEqual(len(response.context["cl"].result_list), 50)

    def test_per_page_query_param_is_respected(self):
        response = self.client.get(self.changelist_url + "?per_page=25")
        self.assertEqual(len(response.context["cl"].result_list), 25)
        self.assertEqual(response.context["cl"].current_per_page, 25)

    def test_per_page_changes_page_contents(self):
        first_small = self.pks_on_page("per_page=25&p=1")
        first_big = self.pks_on_page("per_page=50&p=1")
        self.assertEqual(len(first_small), 25)
        self.assertEqual(len(first_big), 50)
        self.assertEqual(first_small, first_big[:25])

    def test_second_page_does_not_overlap_first(self):
        page1 = set(self.pks_on_page("per_page=25&p=1"))
        page2 = set(self.pks_on_page("per_page=25&p=2"))
        self.assertFalse(page1 & page2)
        self.assertEqual(len(page1 | page2), 50)

    def test_invalid_per_page_falls_back_to_default(self):
        for raw in ("99999", "abc", ""):
            response = self.client.get(f"{self.changelist_url}?per_page={raw}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context["cl"].result_list), 50)

    def test_per_page_is_not_treated_as_a_model_lookup(self):
        """老写法会在这里报“错误的查找参数”。"""
        response = self.client.get(self.changelist_url + "?per_page=25&fullcount=1")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("错误的查找参数", response.content.decode())

    def test_page_links_keep_filters_and_per_page(self):
        response = self.client.get(self.changelist_url + "?per_page=25&flag=1")
        body = response.content.decode()
        self.assertIn("per_page=25", body)
        self.assertIn("下一页", body)

    def test_exact_count_by_default(self):
        response = self.client.get(self.changelist_url)
        self.assertFalse(getattr(response.context["cl"].paginator, "estimated", False))
        self.assertEqual(response.context["cl"].result_count, 120)

    def test_estimated_mode_uses_cursor_pagination(self):
        model_admin = admin_site._registry[TOrders]
        original = model_admin.count_probe_rows
        model_admin.count_probe_rows = 30
        try:
            response = self.client.get(self.changelist_url + "?per_page=25")
            paginator = response.context["cl"].paginator
            self.assertTrue(paginator.estimated)
            self.assertEqual(paginator.count, 31)
            self.assertTrue(paginator.fetched_has_next)

            last = self.client.get(self.changelist_url + "?per_page=25&p=5")
            self.assertEqual(last.status_code, 200)
            self.assertFalse(last.context["cl"].paginator.fetched_has_next)

            exact = self.client.get(self.changelist_url + "?fullcount=1")
            self.assertFalse(exact.context["cl"].paginator.estimated)
            self.assertEqual(exact.context["cl"].result_count, 120)
        finally:
            model_admin.count_probe_rows = original

    def test_no_full_result_count_query_on_big_tables(self):
        response = self.client.get(self.changelist_url)
        self.assertFalse(response.context["cl"].show_full_result_count)


# --------------------------------------------------------------------- 统计条
class ChangelistStatsTests(BaseAdminTest):
    changelist_url = reverse("admin:baccarat_Controll_torders_changelist")

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        make_customer("p1")
        make_orders(30)

    def stats(self, query: str = ""):
        response = self.client.get(f"{self.changelist_url}?{query}")
        self.assertEqual(response.status_code, 200)
        return response.context["stats"]

    def test_totals_follow_the_active_filter(self):
        everything = self.stats("")
        settled = self.stats("flag=1")
        unsettled = self.stats("flag=0")
        self.assertEqual(everything["count"], 30)
        self.assertEqual(settled["count"], 30)
        self.assertEqual(unsettled["count"], 0)
        self.assertEqual(settled["items"][1]["value"], 30 * 1000)

    def test_page_subtotal_only_covers_current_page(self):
        stats = self.stats("per_page=25")
        self.assertEqual(stats["page_rows"], 25)
        page_bet = next(item for item in stats["page_items"] if item["key"] == "bet")
        self.assertEqual(page_bet["value"], 25 * 1000)

    def test_ratio_does_not_crash_on_empty_result(self):
        stats = self.stats("flag=-12345")
        self.assertEqual(stats["count"], 0)
        ratio = next(item for item in stats["items"] if item["key"] == "rate")
        self.assertEqual(ratio["value"], 0)


# --------------------------------------------------------------------- 写路径
class SavePathTests(BaseAdminTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_editing_video_writes_to_database(self):
        """老代码的 change 分支只写 memcache，不写数据库。"""
        video = TVideo.objects.create(videoid="V001", gametype="BJL", bettime=10, url="http://a")
        response = self.client.post(
            reverse("admin:baccarat_Controll_tvideo_change", args=[video.pk]),
            {
                "videoid": "V001",
                "gametype": "BJL",
                "flag": 1,
                "bettime": 20,
                "url": "http://b",
                "_save": "保存",
            },
        )
        self.assertEqual(response.status_code, 302)
        video.refresh_from_db()
        self.assertEqual(video.url, "http://b")
        self.assertEqual(video.bettime, 20)

    def test_agent_save_persists_and_records_ip(self):
        agent_user = User.objects.create_user("agent01", password="pw", is_staff=True)
        agent = TAgents.objects.create(user=agent_user, agentcode=7, agentname="旧名")
        response = self.client.post(
            reverse("admin:userinfo_tagents_change", args=[agent.pk]),
            {
                "user": agent_user.pk,
                "agentcode": 7,
                "agentname": "新名",
                "flag": 1,
                "trytype": 0,
                "_save": "保存",
            },
        )
        self.assertEqual(response.status_code, 302)
        agent.refresh_from_db()
        self.assertEqual(agent.agentname, "新名")
        self.assertEqual(agent.create_ip, "127.0.0.1")

    def test_push_failure_does_not_break_saving(self):
        original = services.push
        services.push = lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("boom"))
        try:
            response = self.client.post(
                reverse("admin:baccarat_Controll_tvideo_add"),
                {
                    "videoid": "V002",
                    "gametype": "BJL",
                    "flag": 0,
                    "bettime": 10,
                    "url": "http://c",
                    "_save": "保存",
                },
            )
        finally:
            services.push = original
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TVideo.objects.filter(videoid="V002").exists())

    def test_round_recalc_action_only_targets_unsettled_rounds(self):
        TRounds.objects.create(roundcode="R1", gametype="BJL", videoid="V001", flag=0, shoecode="S1")
        TRounds.objects.create(roundcode="R2", gametype="BJL", videoid="V001", flag=1, shoecode="S1")
        calls = []
        original = services.recalc_round
        services.recalc_round = lambda code, cards="": calls.append(code) or True
        try:
            response = self.client.post(
                self.url("admin:baccarat_Controll_trounds_changelist"),
                {
                    "action": "recalc_rounds",
                    "_selected_action": ["R1", "R2"],
                    "select_across": 0,
                    "index": 0,
                },
            )
        finally:
            services.recalc_round = original
        self.assertEqual(response.status_code, 302)
        self.assertEqual(calls, ["R1"])


# --------------------------------------------------------------------- 权限与隔离
class PermissionAndScopeTests(BaseAdminTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        make_customer("p1", agentcode=1)
        make_customer("p2", agentcode=2)
        make_orders(3, loginname="p1", start=1)
        make_orders(2, loginname="p2", start=101)
        TOrders.objects.filter(billno__gte=101).update(agentcode=2)
        agent_user = User.objects.create_user("agent01", password="pw", is_staff=True)
        TAgents.objects.create(user=agent_user, agentcode=1, agentname="一号")
        grant_agent_permissions(agent_user)

    def test_readonly_models_have_no_delete_action(self):
        """老代码靠 `del actions['delete_selected']`，在新版会 KeyError。"""
        response = self.client.get(reverse("admin:baccarat_Controll_torders_changelist"))
        self.assertNotContains(response, '<option value="delete_selected"')
        self.assertFalse(admin_site._registry[TOrders].has_delete_permission(self.user))

    def test_agent_only_sees_own_customers(self):
        agent_user = User.objects.get(username="agent01")
        self.client.force_login(agent_user)
        response = self.client.get(reverse("admin:userinfo_tcustomers_changelist"))
        names = [obj.loginname for obj in response.context["cl"].result_list]
        self.assertEqual(names, ["p1"])

    def test_agent_only_sees_own_orders(self):
        agent_user = User.objects.get(username="agent01")
        self.client.force_login(agent_user)
        response = self.client.get(reverse("admin:baccarat_Controll_torders_changelist"))
        self.assertEqual(response.context["cl"].result_count, 3)

    def test_superuser_sees_everything(self):
        response = self.client.get(reverse("admin:userinfo_tcustomers_changelist"))
        self.assertEqual(response.context["cl"].result_count, 2)


# --------------------------------------------------------------------- 过滤器
class FilterTests(BaseAdminTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        make_customer("p1")
        make_orders(10)
        # 一条 40 天前的
        old = TOrders.objects.first()
        old.create_time = timezone.now() - timedelta(days=40)
        old.billno = 999
        old.pk = 999
        old.save(force_insert=True)

    def test_relative_date_filter(self):
        all_count = self.client.get(reverse("admin:baccarat_Controll_torders_changelist")).context["cl"].result_count
        week = self.client.get(
            reverse("admin:baccarat_Controll_torders_changelist") + "?date_range=7d"
        ).context["cl"].result_count
        self.assertEqual(all_count, 11)
        self.assertEqual(week, 10)

    def test_high_cardinality_fields_are_not_filters(self):
        specs = admin_site._registry[TOrders].list_filter
        self.assertNotIn("loginname", specs)
        self.assertNotIn("create_time", specs)
