# -*- coding: utf-8 -*-
"""造演示数据：分页、统计条、过滤器都需要真实量级的数据才能验证。

    python manage.py seed_demo --reset --customers 300 --orders 5000

只用于本地 sqlite（ASIANARK_MANAGED_TABLES=1）。线上老库不要跑。
"""
from __future__ import annotations

import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from AsianarkAdmin.userinfo.models import TAgents, TCustomerTrans, TCustomers
from ...models import (
    TBulletin,
    TOrders,
    TPersonalLimitset,
    TRecalcRounds,
    TRounds,
    TTable,
    TTableLimitset,
    TVideo,
)

GAMES = ["BJL", "DDZ"]


class Command(BaseCommand):
    help = "生成演示数据（本地开发用）"

    def add_arguments(self, parser):
        parser.add_argument("--customers", type=int, default=300)
        parser.add_argument("--orders", type=int, default=5000)
        parser.add_argument("--rounds", type=int, default=300)
        parser.add_argument("--days", type=int, default=30, help="数据分布在最近 N 天内")
        parser.add_argument("--reset", action="store_true", help="先清空相关表")
        parser.add_argument("--seed", type=int, default=20250101)

    @transaction.atomic
    def handle(self, *args, **options):
        rng = random.Random(options["seed"])
        now = timezone.now()
        span = timedelta(days=options["days"])

        if options["reset"]:
            self.stdout.write("清空旧数据…")
            for model in (
                TOrders,
                TRounds,
                TRecalcRounds,
                TCustomerTrans,
                TCustomers,
                TTable,
                TVideo,
                TTableLimitset,
                TPersonalLimitset,
                TBulletin,
            ):
                model.objects.all().delete()

        self._users()
        self._groups()
        limits = self._limits()
        videos = self._videos()
        self._tables(videos, limits)
        customers = self._customers(options["customers"], now, span, rng)
        rounds = self._rounds(options["rounds"], videos, now, span, rng)
        orders = self._orders(options["orders"], customers, rounds, now, span, rng)
        self._trans(customers, now, span, rng)
        self._bulletins(now)
        self._recalc_log(rounds, now, rng)

        self.stdout.write(self.style.SUCCESS(
            f"完成：{TCustomers.objects.count()} 客户 / {TOrders.objects.count()} 注单 / "
            f"{TRounds.objects.count()} 局 / {TCustomerTrans.objects.count()} 流水"
        ))

    # ------------------------------------------------------------------ 账号
    def _users(self):
        for username, password, is_staff in (
            ("admin", "admin123", True),
            ("operator", "operator123", True),
            ("finance", "finance123", True),
            ("agent01", "agent123", True),
        ):
            user, created = User.objects.get_or_create(username=username, defaults={"is_staff": True})
            if created:
                user.set_password(password)
                user.is_superuser = username == "admin"
                user.save()

        agent_user = User.objects.get(username="agent01")
        TAgents.objects.get_or_create(
            agentcode=1,
            defaults={"user": agent_user, "agentname": "一号代理", "flag": 0, "trytype": 0},
        )

    def _groups(self):
        """权限分组：老项目只靠 get_queryset 隔数据，没考虑 admin 自身的权限。"""
        from django.contrib.auth.models import Group, Permission

        groups = {
            "运营": ["view_torders", "change_torders", "view_trounds", "change_trounds",
                    "view_ttable", "change_ttable", "view_tvideo", "change_tvideo",
                    "view_tbulletin", "add_tbulletin", "change_tbulletin"],
            "财务": ["view_tcustomers", "change_tcustomers", "view_tcustomertrans",
                    "change_tcustomertrans", "view_torders"],
            "代理": ["view_tcustomers", "change_tcustomers", "view_tcustomertrans", "view_torders"],
        }
        for name, codenames in groups.items():
            group, _ = Group.objects.get_or_create(name=name)
            group.permissions.set(Permission.objects.filter(codename__in=codenames))

        agent = User.objects.get(username="agent01")
        agent.groups.set(Group.objects.filter(name="代理"))

    def _limits(self):
        created = []
        for index, limitid in enumerate("ABCD", start=1):
            for playtype in range(10):
                row, _ = TTableLimitset.objects.get_or_create(
                    limitid=limitid,
                    playtype=playtype,
                    defaults={"min_cents": 1000, "max_cents": 100_000, "flag": 0},
                )
                TPersonalLimitset.objects.get_or_create(
                    limitid=limitid,
                    playtype=playtype,
                    defaults={"min_cents": 500, "max_cents": 50_000, "flag": 0},
                )
                created.append(row)
        return created

    def _videos(self):
        videos = []
        for index in range(1, 4):
            video, _ = TVideo.objects.get_or_create(
                videoid=f"V{index:03d}",
                defaults={"gametype": "BJL", "bettime": 12, "url": f"http://cdn.example.com/v{index}.m3u8"},
            )
            videos.append(video)
        return videos

    def _tables(self, videos, limits):
        for index in range(1, 8):
            TTable.objects.get_or_create(
                tableid=f"T{index:03d}",
                defaults={
                    "videoid": videos[index % len(videos)],
                    "gametype": "BJL",
                    "limitid": "A",
                    "seats": 7,
                    "flag": 0,
                },
            )

    def _customers(self, count, now, span, rng):
        rows = []
        for index in range(1, count + 1):
            rows.append(
                TCustomers(
                    loginname=f"player{index:05d}",
                    agentcode=1,
                    password="x" * 16,
                    nickname=f"玩家{index:04d}",
                    flag=0,
                    credit_cents=rng.randint(0, 500_000),
                    limitid=rng.choice("ABCD"),
                    create_time=now - timedelta(days=rng.randint(0, 180)),
                    create_ip=f"10.0.{rng.randint(0, 255)}.{rng.randint(1, 254)}",
                    last_login_time=now - timedelta(hours=rng.randint(0, 240)),
                    last_login_ip=f"10.0.{rng.randint(0, 255)}.{rng.randint(1, 254)}",
                    pwd_expired_time=now + timedelta(days=90),
                )
            )
        TCustomers.objects.bulk_create(rows, ignore_conflicts=True)
        return list(TCustomers.objects.values_list("loginname", flat=True))

    def _rounds(self, count, videos, now, span, rng):
        rows = []
        for index in range(1, count + 1):
            started = now - timedelta(minutes=6 * index)
            settled = index % 10 != 0  # 每 10 局留一局未结算，方便测试"重新结算"
            rows.append(
                TRounds(
                    roundcode=f"R{index:08d}",
                    gametype="BJL",
                    videoid=videos[index % len(videos)].videoid,
                    dealer=f"dealer{rng.randint(1, 8):02d}",
                    flag=1 if settled else 0,
                    cards="1,2,3:4,5" if settled else None,
                    cardnum=5 if settled else None,
                    pair=rng.choice([0, 0, 0, 1, 2]),
                    bankerpoint=rng.randint(0, 9) if settled else None,
                    playerpoint=rng.randint(0, 9) if settled else None,
                    begintime=started,
                    closetime=started + timedelta(minutes=1) if settled else None,
                    shoecode=f"S{index // 60:04d}",
                )
            )
        TRounds.objects.bulk_create(rows, ignore_conflicts=True)
        return list(TRounds.objects.values_list("roundcode", flat=True))

    def _orders(self, count, customers, rounds, now, span, rng):
        rows = []
        start = now - span
        for index in range(1, count + 1):
            created = start + timedelta(seconds=rng.randint(0, int(span.total_seconds())))
            bet = rng.choice([1000, 2000, 5000, 10000, 20000, 50000])
            won = rng.random() < 0.45
            win = int(bet * 0.95) if won else -bet
            balance = rng.randint(0, 500_000)
            rows.append(
                TOrders(
                    billno=index,
                    gametype="BJL",
                    loginname=rng.choice(customers),
                    agentcode=1,
                    roundcode=rng.choice(rounds),
                    videoid=f"V{rng.randint(1, 3):03d}",
                    tableid=f"T{rng.randint(1, 7):03d}",
                    seat=rng.randint(0, 6),
                    dealer=f"dealer{rng.randint(1, 8):02d}",
                    flag=1 if rng.random() > 0.02 else 0,
                    playtype=rng.choice([0, 1, 2, 3, 6, 7]),
                    bet_amount_cents=bet,
                    valid_bet_amount_cents=bet,
                    win_amount_cents=win,
                    hashcode="",
                    before_credit_cents=balance,
                    after_credit_cents=balance + win,
                    create_time=created,
                    reckon_time=created + timedelta(seconds=30),
                    create_ip=f"10.0.{rng.randint(0, 255)}.{rng.randint(1, 254)}",
                )
            )
        TOrders.objects.bulk_create(rows, ignore_conflicts=True)
        return count

    def _trans(self, customers, now, span, rng):
        rows = []
        for index in range(1, len(customers) + 1):
            amount = rng.choice([10_000, 50_000, 100_000, -20_000, -50_000])
            rows.append(
                TCustomerTrans(
                    transid=index,
                    action_time=now - timedelta(hours=rng.randint(0, 720)),
                    loginname=rng.choice(customers),
                    agentcode="1",
                    action="充值" if amount > 0 else "提现",
                    trans_amount_cents=amount,
                    before_credit_cents=0,
                    after_credit_cents=amount,
                    remark="seed",
                )
            )
        TCustomerTrans.objects.bulk_create(rows, ignore_conflicts=True)

    def _bulletins(self, now):
        for index in range(1, 6):
            TBulletin.objects.get_or_create(
                text=f"公告 {index}：系统维护通知",
                defaults={"create_time": now - timedelta(days=index), "expired_time": now + timedelta(days=7)},
            )

    def _recalc_log(self, rounds, now, rng):
        rows = [
            TRecalcRounds(
                actionid=index,
                create_time=now - timedelta(hours=rng.randint(1, 500)),
                action=rng.choice(["重新结算局", "取消局注单结算"]),
                roundcode=rng.choice(rounds),
            )
            for index in range(1, 41)
        ]
        TRecalcRounds.objects.bulk_create(rows, ignore_conflicts=True)
