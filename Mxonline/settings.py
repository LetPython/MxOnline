# coding=utf-8
"""
Django settings for Mxonline project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))  # APP放在一起的时候，解决找不到APP的问题
sys.path.insert(0, os.path.join(BASE_DIR, "extra_apps"))  # APP放在一起的时候，解决找不到APP的问题
# Quick-start development settings - unsuitable for
# production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$b$w)86+9*gs8@^d+p%2y#d&hwbkz#q$@k^m5(qkcu2a$st)&t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

AUTHENTICATION_BACKENDS = (  # 重定义 登录验证的 authenticate 方法
    "users.views.CustomBackend",  # 引入在views 中自定义的类
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'courses',
    'organization',
    'operation',
    'xadmin',
    'crispy_forms',
    'captcha',
    'pure_pagination',
]
AUTH_USER_MODEL = "users.UserProfile"  # 重载AUTH方法  app名.类名

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Mxonline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.media',  # Django的media处理类
            ],
        },
    },
]

WSGI_APPLICATION = 'Mxonline.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mxonline',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-hans'  # 中文 显示语言，默认en-us 英语

TIME_ZONE = 'Asia/beijing'  # 设置为北京时区  默认UTC

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 默认为True，默认取UTC 的时间。修改时间时要改为False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# 邮箱配置
EMAIL_HOST = "smtp.sina.com"  # 配置邮件发送地址，该地址可在新浪邮箱的客户端设置里找到 SMTP服务器：smtp.sina.com
EMAIL_PORT = 25  # 配置邮件的端口
EMAIL_HOST_USER = "xinxinainixd@sina.com"
EMAIL_HOST_PASSWORD = "XINxinAIziJI0328"
EMAIL_USE_TLS = False
EMAIL_FROM = "xinxinainixd@sina.com"  # 指明发件人

# 上传图片的路径配置
MEDIA_URL = '/static/media/'  # 在模板语言中引用
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')  # 只能设置一个路径

