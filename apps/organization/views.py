# _*_ encoding:utf-8 _*_
import json

from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, City, Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite


# Create your views here.


class OrgView(View):
    """
    课程机构列表
    """

    def get(self, request):
        all_orgs = CourseOrg.objects.all()  # 课程机构
        hot_orgs = all_orgs.order_by("-click_num")[:3]  # 前三个热门机构
        all_citys = City.objects.all()  # 城市

        # 机构搜索
        search_keywords = request.GET.get("keywords", '')  # 搜索关键词
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 根据学生人数和课程数排序
        sort = request.GET.get("sort", '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()  # 显示机构的数量统计

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {"all_orgs": orgs,
                                                 "all_citys": all_citys,
                                                 "org_nums": org_nums,
                                                 'city_id': city_id,
                                                 'category': category,
                                                 'hot_orgs': hot_orgs,
                                                 'sort': sort}
                      )


class AddUserAskView(View):
    """
    用户添加咨询
    """

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        response = {'status': 'success'}
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)  # modelform 有的方法，直接提交到数据库中
            return HttpResponse(json.dumps(response), content_type='application/json')  # 返回的是json格式的字符串，写法是固定的
        else:
            response['status'] = 'fail'
            response['msg'] = '添加出错'
            return HttpResponse(json.dumps(response), content_type='application/json')


class OrgHomeView(View):
    """
    机构详情首页
    """

    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_course = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html',
                      {"all_courses": all_course,
                       "all_teacher": all_teacher,
                       "course_org": course_org,
                       "current_page": current_page,
                       "has_fav": has_fav,
                       }
                      )


class OrgCourseView(View):
    """
    机构课程列表页
    """

    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_course = course_org.course_set.all()
        return render(request, 'org-detail-course.html',
                      {"all_courses": all_course,
                       "course_org": course_org,
                       "current_page": current_page,
                       "has_fav": has_fav,
                       }
                      )


class OrgDescView(View):
    """
    机构介绍
    """

    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html',
                      {"course_org": course_org, "current_page": current_page, "has_fav": has_fav, }
                      )


class OrgTeacherView(View):
    """
    机构教师页
    """

    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html',
                      {"all_teachers": all_teachers,
                       "course_org": course_org,
                       "current_page": current_page,
                       "has_fav": has_fav,
                       }
                      )


class AddFavView(View):
    """
    用户收藏，取消收藏
    """

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        response = {'status': 'success'}
        if not request.user.is_authenticated():  # 判断用户是否已经登录，内置的方法,未登录。
            response['status'] = 'fail'
            response['msg'] = '用户未登录'
            return HttpResponse(json.dumps(response), content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id),
                                                    fav_type=int(fav_type))  # 查找收藏记录
        if exist_records:  # 如果已经收藏，就取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_num -= 1
                if course_org.fav_num < 0:
                    course_org.fav_num = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_num -= 1
                if teacher.fav_num < 0:
                    teacher.fav_num = 0
                teacher.save()
            response['msg'] = '收藏'
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_num += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_num += 1
                    teacher.save()
                response['msg'] = '已收藏'
                return HttpResponse(json.dumps(response), content_type='application/json')
            else:
                response['status'] = 'fail'
                response['msg'] = '收藏出错'
                return HttpResponse(json.dumps(response), content_type='application/json')


class TeacherListView(View):
    """
    课程讲师列表页
    """

    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 讲师搜索
        search_keywords = request.GET.get("keywords", '')  # 搜索关键词
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords) | Q(
                    work_position__icontains=search_keywords))

        # 根据人气排序
        sort = request.GET.get("sort", '')
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_num")

        # 右侧讲师排行榜,前三名
        sorted_teachers = Teacher.objects.all().order_by("-click_num")[:3]

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 2, request=request)
        teachers = p.page(page)

        teachers_nums = all_teachers.count()
        return render(request, "teachers-list.html", {
            "all_teachers": teachers,
            "sorted_teachers": sorted_teachers,
            "teachers_nums": teachers_nums,
            "sort": sort,
        })


class TeacherDetailView(View):
    """
    课程讲师信息页
    """

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_num += 1
        teacher.save()
        all_courses = teacher.course_set.all()
        org_teacher = teacher.org
        # 右侧讲师排行榜,前三名
        sorted_teachers = Teacher.objects.all().order_by("-click_num")[:3]

        # 判断是否收藏
        teacher_has_fav = False
        org_has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                teacher_has_fav = True
            elif UserFavorite.objects.filter(user=request.user, fav_id=org_teacher.id, fav_type=2):
                org_has_fav = True

        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "sorted_teachers": sorted_teachers,
            "all_courses": all_courses,
            "org_teacher": org_teacher,
            "teacher_has_fav": teacher_has_fav,
            "org_has_fav": org_has_fav,
        })
