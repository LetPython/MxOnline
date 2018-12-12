# coding=utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser  # 导入Django默认的user表


# Create your models here.

class UserProfile(AbstractUser):
    """
    自己创建的user表，继承Django默认的user表
    """
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default=u"")  # 昵称
    birday = models.DateField(verbose_name=u'生日', null=True, blank=True)  # 生日
    gender = models.CharField(max_length=16, choices=(("male", u'男'), ("female", u'女')), default="female")  # 性别
    address = models.CharField(max_length=100, default=u"")  # 地址
    mobile = models.CharField(max_length=11, null=True, blank=True)  # 手机号
    image = models.ImageField(upload_to="image/%Y/%m", default=u'image/default.png', max_length=100)  # 头像

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):  # 相当于Python3 的 __str__
        return self.username


class EmailVerifyRecord(models.Model):
    """
    邮箱验证码
    """
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(max_length=10, choices=(('register', u'注册'), ('forget', u'找回')))  # 验证码的类型，注册时和找回时
    send_time = models.DateTimeField(default=datetime.now)  # 发送的时间

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    """
    轮播图
    """
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(max_length=100, upload_to="banner/%Y/%m", verbose_name=u"轮播图")
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"播放顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name
