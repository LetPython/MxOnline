#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2018/12/13 11:34'

"""
自定义 form 组件
"""

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    """
    登录form表单验证
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    """
    注册form验证及验证码
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetForm(forms.Form):
    """
    找回密码form验证及验证码
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyForm(forms.Form):
    """
    重置密码form验证及验证码
    """
    password1 = forms.CharField(required=True, min_length=6, error_messages={"min_length": u"不能少于6位"})
    password2 = forms.CharField(required=True, min_length=6, error_messages={"min_length": u"不能少于6位"})


class UploadImageForm(forms.ModelForm):
    """
    用户修改头像
    """
    class Meta:
        model = UserProfile  # 指明是用那个model转换的modelform
        fields = ["image"]  # 需要选择转换的字段


class UserInfoForm(forms.ModelForm):
    """
    用户信息修改
    """
    class Meta:
        model = UserProfile  # 指明是用那个model转换的modelform
        fields = ["nick_name", "gender", "birday", "address", "mobile"]  # 需要选择转换的字段