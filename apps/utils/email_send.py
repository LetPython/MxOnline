#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2018/12/13 16:12'

"""
给用户发送邮件
"""
from random import Random
from django.core.mail import send_mail  # 发送邮箱函数

from users.models import EmailVerifyRecord
from Mxonline.settings import EMAIL_FROM  # 引入在settings.py 里配置的 发送人


def random_str(randomlenth=8):
    """
    默认生成随机8位字符串
    :param randomlenth: 字符串长度
    :return: 随机字符串
    """
    str = ""
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlenth):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):
    """
    发送注册验证邮件
    :param email: 邮箱
    :param send_type: 邮件类型,默认注册
    :return:
    """
    # 将邮箱验证码，邮箱，类型等保存到数据库
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    # 编辑要发送的内容
    email_title = ""  # 邮件的标题
    email_body = ""  # 邮件正文

    if send_type == "register":
        email_title = "慕学在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 调用发送邮件函数，并返回布尔值
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "慕学在线网密码重置链接"
        email_body = "请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 调用发送邮件函数，并返回布尔值
        if send_status:
            pass
