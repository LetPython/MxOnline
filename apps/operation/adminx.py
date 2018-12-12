#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2018/12/12 19:37'

import xadmin

from .models import CourseComments, UserAsk, UserCourse, UserFavorite, UserMessage


class CourseCommentsAdmin(object):
    list_display = ["user", "course", "comment", "add_time"]
    search_fields = ["user", "course", "comment"]
    list_filter = ["user", "course", "comment", "add_time"]


class UserCourseAdmin(object):
    list_display = []
    list_filter = []
    search_fields = []


class UserAskAdmin(object):
    list_display = ["name", "mobile", "course_name", "add_time"]
    list_filter = ["name", "mobile", "course_name", "add_time"]
    search_fields = ["name", "mobile", "course_name"]


class UserFavoriteAdmin(object):
    list_display = ["user", "fav_id", "fav_type", "add_time"]
    list_filter = ["user", "fav_id", "fav_type", "add_time"]
    search_fields = ["user", "fav_id", "fav_type"]


class UserMessageAdmin(object):
    list_display = ["user", "message", "has_read", "add_time"]
    list_filter = ["user", "message", "has_read", "add_time"]
    search_fields = ["user", "message", "has_read"]


xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
