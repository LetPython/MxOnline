# _*_ encoding:utf-8 _*_
import json

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout  # 登录验证
from django.contrib.auth.backends import ModelBackend  # 修改 authenticate 验证 邮箱登录时用
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.views.generic.base import View  # CBV
from django.contrib.auth.hashers import make_password  # 密码加密函数
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import UserProfile, EmailVerifyRecord, Banner  # 导入model
from .form import LoginForm, RegisterForm, ForgetForm, ModifyForm, UploadImageForm, UserInfoForm  # 导入自定义的form
from utils.email_send import send_register_email  # 导入自定义的  注册发送邮箱
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course


# Create your views here.
class CustomBackend(ModelBackend):
    """
    修改 authenticate 验证 邮箱登录
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 用户名或密码登录
            if user.check_password(password):  # 判断将明文的密码转换后和密文的密码是否一致
                return user
        except Exception as e:
            return None

class LogoutView(View):
    """
    退出
    """
    def get(self,request):
        logout(request)

        return redirect(reverse("index"))

class LoginView(View):
    """
    登录
    """

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login_form = LoginForm(request.POST)  # 表单验证
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)  # 验证登录
            if user is not None:
                if user.is_active:
                    login(request, user)  # 完成login登录，并完成session操作
                    return redirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": u"用户未激活"})
            else:
                return render(request, "login.html", {"msg": u"用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class RegisterView(View):
    """
    注册
    """

    def get(self, request):
        register_form = RegisterForm()  # 用于HTML生成form
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get("email", "")
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {"register_form": register_form, "msg": "用户已经存在"})
            password = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.is_active = False  # 判断是否已经激活用
            user_profile.password = make_password(password)  # 密码加密后保存
            user_profile.save()
            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕学在线网"
            user_message.save()

            send_register_email(username, "register")  # 调用发送邮件函数
            return redirect("login")
        else:
            return render(request, 'register.html', {"register_form": register_form})


class ActiveView(View):
    """
    激活
    """

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ForgetPwdView(View):
    """
    找回密码
    """

    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            if UserProfile.objects.filter(email=email):
                send_register_email(email, send_type="forget")
                return render(request, 'send_success.html')
            else:
                return render(request, 'forgetpwd.html', {"msg": "用户不存在", "forget_form": forget_form})
        else:
            return render(request, 'forgetpwd.html', {"forget_form": forget_form})


class ResetView(View):
    """
    重置密码
    """

    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {"email": email})
        else:
            return render(request, 'reset_fail.html')


class ModifyPwdView(View):
    """
    重置修改密码
    """

    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            email = request.POST.get("email", "")
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 != password2:
                return render(request, 'password_reset.html', {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get("email", "")
            return render(request, 'password_reset.html', {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """

    def get(self, request):
        return render(request, "usercenter-info.html")

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)  # 指定是哪个实例（指定用户，不知道会新创建）
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(json.dumps({"status": "success"}))
        else:
            return HttpResponse(json.dumps(user_info_form.errors))


class ImageUploadView(LoginRequiredMixin, View):
    """
    用户修改头像
    """

    def post(self, request):
        image_upload_form = UploadImageForm(request.POST, request.FILES,
                                            instance=request.user)  # modelform，具有model和form的双重特性。
        response = {"status": "success"}
        if image_upload_form.is_valid():
            image_upload_form.save()
            return HttpResponse(json.dumps(response))
        else:
            response["status"] = "fail"
            return HttpResponse(json.dumps(response))


class UpdatePwdView(View):
    """
    个人中心修改密码
    """

    def post(self, request):
        modify_form = ModifyForm(request.POST)
        response = {'status': 'success'}
        if modify_form.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 != password2:
                response['status'] = 'fail'
                response['msg'] = '密码不一致'
                return HttpResponse(json.dumps(response))
            user = request.user
            user.password = make_password(password1)
            user.save()
            return HttpResponse(json.dumps(response))
        else:
            return HttpResponse(json.dumps(modify_form.errors))


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """

    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse(json.dumps({"email": "邮箱已经存在"}))
        send_register_email(email, send_type="update")
        return HttpResponse(json.dumps({"status": "success"}))


class UpdateEmailView(View):
    """
    修改个人邮箱
    """

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update")
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse(json.dumps({"status": "success"}))
        else:
            return HttpResponse(json.dumps({"email": "验证码错误"}))


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            "user_courses": user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我的收藏,机构
    """

    def get(self, request):
        org_list = []
        user_fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for user_fav_org in user_fav_orgs:
            org_fav_id = user_fav_org.fav_id
            org = CourseOrg.objects.get(id=org_fav_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,

        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我的收藏,讲师
    """

    def get(self, request):
        teacher_list = []
        user_fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for user_fav_teacher in user_fav_teachers:
            teacher_fav_id = user_fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_fav_id)
            teacher_list.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list
        })

class MyFavCourseView(LoginRequiredMixin, View):
    """
    我的收藏,课程
    """

    def get(self, request):
        course_list = []
        user_fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for user_fav_course in user_fav_courses:
            course_fav_id = user_fav_course.fav_id
            course = Course.objects.get(id=course_fav_id)
            course_list.append(course)
        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list
        })



class MyMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """

    def get(self, request):
        user_messgaes = UserMessage.objects.filter(user=request.user.id)
        all_unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)  # 用户进入后把所有的消息设为已读
        for unread_massage in all_unread_message:
            unread_massage.has_read = True
            unread_massage.save()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(user_messgaes, 2, request=request)
        messages = p.page(page)

        return render(request, "usercenter-message.html", {
            "user_messgaes": messages,
        })


class IndexView(View):
    def get(self, request):
        # print 1/0  # 当代码出现错误时弹出500页面

        all_banners = Banner.objects.all().order_by("index")  # 取出轮播图
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_course = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {
            "all_banners": all_banners,
            "courses": courses,
            "banner_course": banner_course,
            "course_orgs": course_orgs


        })


def page_not_found(request):
    """
    全局404页面处理函数
    """
    from django.shortcuts import render_to_response
    response = render_to_response('404.html')
    response.status_code = 404  # 设置状态码为404
    return response

def page_error(request):
    """
    全局500页面处理函数
    """
    from django.shortcuts import render_to_response
    response = render_to_response('500.html')
    response.status_code = 500  # 设置状态码为404
    return response