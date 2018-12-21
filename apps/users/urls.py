#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2018/12/19 18:04'

from django.conf.urls import url

import views

urlpatterns = [
    url(r'^info/$', views.UserInfoView.as_view(), name="user_info"),  # 用户个人信息
    url(r'^image/upload/$', views.ImageUploadView.as_view(), name="image_upload"),  # 用户头像修改
    url(r'^update/pwd/$', views.UpdatePwdView.as_view(), name="update_pwd"),  # 用户密码修改
    url(r'^sendemail_code/$', views.SendEmailCodeView.as_view(), name="sendemail_code"),  # 用户邮箱修改发送验证码
    url(r'^update_email/$', views.UpdateEmailView.as_view(), name="update_email"),  # 用户邮箱修改

    url(r'^mycourse/$', views.MyCourseView.as_view(), name="mycourse"),  # 我的课程
    url(r'^myfav/org$', views.MyFavOrgView.as_view(), name="myfav_org"),  # 我的收藏, 机构
    url(r'^myfav/teacher$', views.MyFavTeacherView.as_view(), name="myfav_teacher"),  # 我的收藏, 讲师
    url(r'^myfav/course$', views.MyFavCourseView.as_view(), name="myfav_course"),  # 我的收藏, 课程
    url(r'^mymessage/$', views.MyMessageView.as_view(), name="mymessage"),  # 我的消息

]