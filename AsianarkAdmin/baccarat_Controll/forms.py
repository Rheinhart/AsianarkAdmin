#coding:utf8
"""
@__author__ = 'Thomas'
"""
from django.forms import ModelForm
from AsianarkAdmin.suit.widgets import SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget
from models import TBulletin

class TBulletinForm(ModelForm):
    class Meta:
        model = TBulletin
        fields = '__all__'
        widgets = {
            'create_time': SuitSplitDateTimeWidget,
            'expired_time': SuitSplitDateTimeWidget,
        }