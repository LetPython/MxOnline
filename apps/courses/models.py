# coding=utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher


# Create your models here.


class Course(models.Model):
    """
    课程
    """
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)
    degree = models.CharField(choices=(("cj", u"初级"), ('zj', u"中级"), ("gj", u"高级")), max_length=2, verbose_name=u"难度")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟）")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(max_length=20, verbose_name=u"课程类别", default=u'后端开发')
    tag = models.CharField(default='', verbose_name=u"课程标签", max_length=10)
    youneed_know = models.CharField(max_length=300, verbose_name=u"课程须知", default='')
    teacher_tell = models.CharField(max_length=300, verbose_name=u"老师告诉你", default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_lesson_nums(self):
        return self.lesson_set.all().count()  # 获取课程章节数

    def get_learn_user(self):  # 获取学习课程的用户
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):  # 获取课程章节
        return self.lesson_set.all()

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    """
    章节信息
    """
    course = models.ForeignKey(Course, verbose_name=u"课程")  # 外键指向课程
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_video(self):  # 获取视频信息
        return self.video_set.all()


class Video(models.Model):
    """
    视频
    """
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")  # 外键指向章节
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟）")

    url = models.CharField(max_length=200,default="", verbose_name=u"访问地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    """
    课程资源链接下载
    """
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name  # 复数形式

    def __unicode__(self):
        return self.name
