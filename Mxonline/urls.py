# _*_ encoding:utf-8 _*_

"""Mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin

from users import views

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),  # 首页
    url(r'^login/$', views.LoginView.as_view(), name="login"),  # 登录页
    url(r'^register/$', views.RegisterView.as_view(), name="register"),  # 注册
    url(r'^captcha/', include('captcha.urls')),  # 生成验证码的插件
    url(r'^active/(?P<active_code>[a-zA-Z0-9]{16})/$', views.ActiveView.as_view(), name="user_active"),  # 用户激活
    url(r'^forget/$', views.ForgetPwdView.as_view(), name="forget_pwd"),  # 找回密码
    url(r'^reset/(?P<reset_code>[a-zA-Z0-9]{16})/$', views.ResetView.as_view(), name="reset_pwd"),  # 重置密码
    url(r'^modify/$', views.ModifyPwdView.as_view(), name="modify_pwd"),  # 重置密码提交路径

]
