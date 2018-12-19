#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2018/12/17 17:43'

import re

from django import forms

from operation.models import UserAsk


# form表单
# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=5, max_length=50)


# modelform表单
class UserAskForm(forms.ModelForm):
    """
    我要学习 , 用户咨询
    """

    # 此处还可以定义额外的字段

    class Meta:
        model = UserAsk  # 指明是用那个model转换的modelform
        fields = ["name", "mobile", "course_name"]  # 需要选择转换的字段

    def clean_mobile(self):  # 定义手机号验证
        mobile = self.cleaned_data['mobile']  # 取出mobile
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")  # 主动抛出异常信息，code是自己定义
