#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2018/12/12 19:52'

import xadmin

from .models import Course, CourseResource, Lesson, Video, BannerCourse
from organization.models import CourseOrg

class LessonInline(object):
    """在增加课程的时候增加章节"""
    model = Lesson  # 指定要增加的model
    extra = 0

class CourseResourceInline(object):
    model = CourseResource
    extre = 0


class CourseAdmin(object):
    list_display = ["course_org", "name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums",
                    "add_time", "get_lesson_nums", "go_to"]
    list_filter = ["course_org", "name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "click_nums",
                   "add_time"]
    search_fields = ["course_org", "name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums"]

    ordering = ["-click_nums"]  # 设置默认排序的字段

    readonly_fields = [ "click_nums", "students"]  # 设置字段为只读
    exclude = ["fav_nums"]  # 设置字段隐藏不在后台管理中显示  # 当 readonly_fields 和 exclude 都设置了同一个字段时是不生效的

    inlines = [LessonInline, CourseResourceInline]  # 可以在增加课程的时候增加章节和课程资源的操作。 要先定义一个指定的类

    list_editable = ["degree", "desc"]  # 可以设置该字段在列表页直接编辑

    refresh_times = [3, 5]  # 设置选择每3秒或每5秒后自动刷新页面

    style_fields = {"detail": "ueditor"}  # 指明字段使用的样式，这里是指明detail 为富文本样式

    import_excel = True  # 设置导入插件Excel

    def save_models(self):
        """每次进行save时的操作，在保存课程的时候统计课程机构的课程数"""
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)

    def queryset(self):
        """进行数据过滤，管理特定的数据"""
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

class BannerCourseAdmin(object):
    """"""
    list_display = ["course_org", "name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums",
                    "add_time"]
    list_filter = ["course_org", "name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "click_nums",
                   "add_time"]
    search_fields = ["course_org", "name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums"]

    ordering = ["-click_nums"]  # 设置默认排序的字段

    readonly_fields = [ "click_nums", "students"]  # 设置字段为只读
    exclude = ["fav_nums"]  # 设置字段隐藏不在后台管理中显示  # 当 readonly_fields 和 exclude 都设置了同一个字段时是不生效的

    inlines = [LessonInline, CourseResourceInline]  # 可以在增加课程的时候增加章节和课程资源的操作。 要先定义一个指定的类

    def queryset(self):
        """进行数据过滤，管理特定的数据"""
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs



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
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
