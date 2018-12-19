#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2018/12/12 19:25'

import xadmin

from .models import City, CourseOrg, Teacher


class CityAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ["name", "desc", "category", "click_num", "fav_num", "image", "address", "city", "add_time"]
    search_fields = ["name", "desc", "category", "click_num", "fav_num", "image", "address", "city"]
    list_filter = ["name", "desc", "category", "click_num", "fav_num", "image", "address", "city", "add_time"]


class TeacherAdmin(object):
    list_display = ["org", "name", "work_years", "work_company", "work_position", "points", "click_num", "fav_num",
                    "add_time"]
    search_fields = ["org", "name", "work_years", "work_company", "work_position", "points", "click_num", "fav_num"]
    list_filter = ["org", "name", "work_years", "work_company", "work_position", "points", "click_num", "fav_num",
                   "add_time"]


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
