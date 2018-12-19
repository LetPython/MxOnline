#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2018/12/17 17:52'

from django.conf.urls import url

import views

urlpatterns = [
    url(r'^list/$', views.OrgView.as_view(), name="org_list"),  # 课程机构首页
    url(r'^add_ask/$', views.AddUserAskView.as_view(), name="add_ask"),  # 添加用户咨询
    url(r'^home/(?P<org_id>\d+)/$', views.OrgHomeView.as_view(), name="org_home"),  # 机构详情首页
    url(r'^course/(?P<org_id>\d+)/$', views.OrgCourseView.as_view(), name="org_course"),  # 机构课程
    url(r'^desc/(?P<org_id>\d+)/$', views.OrgDescView.as_view(), name="org_desc"),  # 机构介绍
    url(r'^teacher/(?P<org_id>\d+)/$', views.OrgTeacherView.as_view(), name="org_teacher"),  # 机构讲师
    url(r'^add_fav/$', views.AddFavView.as_view(), name="add_fav"),  # 添加机构收藏
    url(r'^teacher/list/$', views.TeacherListView.as_view(), name="teacher_list"),  # 讲师列表页
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', views.TeacherDetailView.as_view(), name="teacher_detail"),  # 讲师详情页

]

