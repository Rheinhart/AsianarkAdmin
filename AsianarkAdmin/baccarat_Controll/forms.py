# -*- coding: utf-8 -*-
"""表单。

老版本只是为了换 suit 的日期控件（`SuitSplitDateTimeWidget`）—— Django admin 对
DateTimeField 本来就用 `AdminSplitDateTime`，不需要自定义控件。这里保留表单是为了
真正的业务校验：公告到期时间必须晚于创建时间。
"""
from django import forms

from .models import TBulletin


class TBulletinForm(forms.ModelForm):
    class Meta:
        model = TBulletin
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        create, expired = cleaned.get("create_time"), cleaned.get("expired_time")
        if create and expired and expired <= create:
            raise forms.ValidationError("到期时间必须晚于创建时间")
        return cleaned
