#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2018/12/18 12:32'

from django.conf.urls import url

import views

urlpatterns = [
    url(r'^list/$', views.CourseListView.as_view(), name="course_list"),  # 课程列表首页
    url(r'^detail/(?P<course_id>\d+)/$', views.CourseDetailView.as_view(), name="course_detail"),  # 课程详情页
    url(r'^info/(?P<course_id>\d+)/$', views.CourseInfoView.as_view(), name="course_info"),  # 课程章节信息页
    url(r'^comment/(?P<course_id>\d+)/$', views.CourseCommentView.as_view(), name="course_comment"),  # 课程评论页
    url(r'^add_comment/$', views.AddCommentView.as_view(), name="add_comment"),  # 添加课程评论
    url(r'^video/(?P<video_id>\d+)/$', views.VideoPlayView.as_view(), name="video_play"),  # 课程详情页

]