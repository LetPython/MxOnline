# _*_ encoding:utf-8 _*_

from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login  # 登录验证
from django.contrib.auth.backends import ModelBackend  # 修改 authenticate 验证 邮箱登录时用
from django.db.models import Q
from django.views.generic.base import View  # CBV
from django.contrib.auth.hashers import make_password  # 密码加密函数

from .models import UserProfile, EmailVerifyRecord  # 导入model
from .form import LoginForm, RegisterForm, ForgetForm, ModifyForm  # 导入自定义的form
from utils.email_send import send_register_email  # 导入自定义的  注册发送邮箱


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
                    return render(request, "index.html")
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
            send_register_email(username, "register")  # 调用发送邮件函数
            return render(request, 'login.html')
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
