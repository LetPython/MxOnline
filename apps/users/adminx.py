#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'  # 作者
__date__ = '2018/12/12 17:22'  # 时间

import xadmin
from xadmin import views
# from xadmin.plugins.auth import UserAdmin
from .models import EmailVerifyRecord, Banner, UserProfile


# class UserProfileAdmin(UserAdmin):
#     pass


class BaseSetting(object):
    """
    主题配置
    """
    enable_themes = True  # 主题功能，默认False取消掉了
    use_bootswatch = True  # 使用更多的主题样式


class GlobalSettings(object):
    """
    全局设置
    """
    site_title = "慕学后台管理系统"  # 页面左上角
    site_footer = "慕学在线网"  # 页面最底部的文字
    menu_style = "accordion"  # 设置左侧菜单栏 折叠


class EmailVerifyRecordAdmin(object):
    list_display = ["code", "email", "send_type", "send_time"]  # 设置页面默认显示的列
    search_fields = ["code", "email", "send_type"]  # 设置页面搜索字段，不能对时间搜索
    list_filter = ["code", "email", "send_type", "send_time"]  # 设置筛选字段
    model_icon = 'fa fa-envelope-o'  # 后台管理系统的左侧列表的图标设置


class BannerAdmin(object):
    list_display = ["title", "image", "url", "index", "add_time"]  # 设置页面默认显示的列
    search_fields = ["title", "image", "url", "index"]  # 设置页面搜索字段，不能对时间搜索
    list_filter = ["title", "image", "url", "index", "add_time"]  # 设置筛选字段


# from django.contrib.auth.models import User
# xadmin.site.unregister(User)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
