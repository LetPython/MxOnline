#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2018/12/12 19:52'

import xadmin

from .models import Course, CourseResource, Lesson, Video


class CourseAdmin(object):
    list_display = ["course_org", "name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums",
                    "add_time"]
    list_filter = ["course_org", "name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "click_nums",
                   "add_time"]
    search_fields = ["course_org", "name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums"]


class CourseResourceAdmin(object):
    list_display = ["course", "name", "download", "add_time"]
    list_filter = ["course", "name", "download", "add_time"]
    search_fields = ["course", "name", "download"]


class LessonAdmin(object):
    list_display = ["course", "name", "add_time"]
    list_filter = ["course__name", "name", "add_time"]  # course__name 是外键跨表查询
    search_fields = ["course__name", "name"]  # course__name 是外键跨表查询


class VideoAdmin(object):
    list_display = ["lesson", "name", "add_time"]
    list_filter = ["lesson", "name", "add_time"]
    search_fields = ["lesson", "name"]


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
