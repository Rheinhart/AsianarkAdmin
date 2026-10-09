# -*- coding: utf-8 -*-
"""客户 / 资金流水 / 代理模型（对应老库 t_customers / t_customer_trans / t_agents）。

表结构属于老库（managed=False）；本地开发用 `manage.py init_local_db` 建表。
"""
from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from AsianarkAdmin.tools.choicecode import FLAG, LIMITID, TRYTYPE


class TCustomers(models.Model):
    """玩家账户。"""

    loginname = models.CharField(
        db_column="Loginname", verbose_name="用户名", max_length=32, primary_key=True
    )
    agentcode = models.IntegerField(db_column="AgentCode", verbose_name="代理CODE", db_index=True)
    password = models.CharField(max_length=32, verbose_name="密码")
    nickname = models.CharField(max_length=32, verbose_name="昵称")
    flag = models.IntegerField(db_column="Flag", verbose_name="是否禁用", choices=FLAG, default=0)
    credit_cents = models.IntegerField(db_column="Credit_cents", verbose_name="信用额度", default=0)
    limitid = models.CharField(
        db_column="limitID", choices=LIMITID, verbose_name="个人限红ID", max_length=4
    )
    create_time = models.DateTimeField(
        db_column="Create_time", verbose_name="创建时间", default=timezone.now, db_index=True
    )
    create_ip = models.GenericIPAddressField(
        db_column="Create_ip", max_length=39, verbose_name="创建IP"
    )
    last_login_time = models.DateTimeField(
        db_column="Last_login_time", verbose_name="最后一次登录时间", blank=True, null=True
    )
    last_login_ip = models.GenericIPAddressField(
        db_column="Last_login_ip", max_length=39, verbose_name="最后一次登录IP", blank=True, null=True
    )
    pwd_expired_time = models.DateTimeField(
        db_column="Pwd_expired_time", verbose_name="密码失效时间", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t_customers"
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"
        ordering = ("-create_time", "loginname")
        indexes = [
            models.Index(fields=["agentcode", "-create_time"], name="t_customers_agent_idx"),
            models.Index(fields=["nickname"], name="t_customers_nick_idx"),
        ]

    def __str__(self):
        return f"{self.loginname}（{self.nickname}）"


class TCustomerTrans(models.Model):
    """额度变动流水（充值/提现/转账）。"""

    transid = models.IntegerField(primary_key=True, verbose_name="序列号")
    action_time = models.DateTimeField(
        db_column="Action_time", verbose_name="操作执行时间", default=timezone.now, db_index=True
    )
    loginname = models.CharField(max_length=16, verbose_name="用户名", db_index=True)
    agentcode = models.CharField(db_column="AgentCode", verbose_name="代理CODE", max_length=16)
    action = models.CharField(max_length=32, verbose_name="操作")
    trans_amount_cents = models.IntegerField(
        db_column="Trans_amount_Cents", verbose_name="转账额度", default=0
    )
    before_credit_cents = models.IntegerField(
        db_column="Before_credit_Cents", verbose_name="操作前额度", default=0
    )
    after_credit_cents = models.IntegerField(
        db_column="After_credit_Cents", verbose_name="操作后额度", default=0
    )
    remark = models.CharField(max_length=100, verbose_name="附注", blank=True)

    class Meta:
        managed = False
        db_table = "t_customer_trans"
        verbose_name = "用户额度记录"
        verbose_name_plural = "用户额度记录"
        ordering = ("-transid",)
        indexes = [
            models.Index(fields=["loginname", "-action_time"], name="t_ctrans_user_time_idx"),
        ]

    def __str__(self):
        return f"{self.transid} {self.loginname} {self.action}"


class TAgents(models.Model):
    """代理（与后台账号一对一绑定，用于数据隔离）。"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="agent", verbose_name="后台账号"
    )
    agentcode = models.IntegerField(db_column="AgentCode", primary_key=True, verbose_name="代理CODE")
    agentname = models.CharField(db_column="AgentName", max_length=32, verbose_name="代理名")
    flag = models.IntegerField(verbose_name="是否禁用", choices=FLAG, default=0)
    trytype = models.IntegerField(db_column="Try_Type", verbose_name="是否试用", choices=TRYTYPE, default=0)
    create_time = models.DateTimeField(
        db_column="Create_time", default=timezone.now, verbose_name="创建时间"
    )
    create_ip = models.GenericIPAddressField(
        db_column="Create_ip", max_length=39, verbose_name="创建IP", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t_agents"
        verbose_name = "代理信息"
        verbose_name_plural = "代理信息"
        ordering = ("agentcode",)

    def __str__(self):
        return f"{self.agentcode} {self.agentname}"
