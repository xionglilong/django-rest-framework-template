"""
版本 Django 4.0.6.
文档：https://docs.djangoproject.com/en/4.0/topics/settings/
文档：https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 将apps文件夹添加到包搜索路径（注意在IDE中也要手动添加apps为源代码根目录）
# sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 安全警告: 在正式环境中请保守密钥
SECRET_KEY = 'django-insecure-1^#p1(k=0cf=04xi_2m7hd&zi)5jiskkippq98dvkk2h&gzegc'

# 安全警告: 不要在正式环境中打开DEBUG开关
DEBUG = True

ALLOWED_HOSTS = []

# App配置
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',  # 添加过滤器包(django-filter)
    'drf_spectacular',  # 自动生成api文档
    'users.apps.UsersConfig',
    'persons.apps.PersonsConfig',
]

# rest_framework的全局配置
REST_FRAMEWORK = {
    # 分页功能的全局设置
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # 修改默认的分页类型，使用每页数量和页面编号来分页
    'PAGE_SIZE': 20,  # 每个页面的数量，配置完后立马有分页功能，并且json数据格式会调整，还会多出几个字段：count、next、previous，文件路径字段还会添加完整域名

    'DEFAULT_AUTHENTICATION_CLASSES': (  # 类似于中间件，按顺序执行authenticate()，主要是通过不同的认证方式来查找用户并设置request.user
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # 依赖django的SessionMiddleware、AuthenticationMiddleware，一般浏览器常见，前后端分离一般不用，不过内置文档功能要用
        # 'rest_framework_simplejwt.authentication.JWTAuthentication', # 这里是全局做 jwt接收到request.user的转换，有些api是不需要登录的，所以一般也不在这配，仅作演示
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # drf-spectacular api文档配置
}

# drf-spectacular api文档配置: https://github.com/tfranzel/drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'API接口文档',
    'DESCRIPTION': '项目详情介绍',
    'VERSION': '1.0.0',
    # OTHER SETTINGS
}


# 自定义用户模型
AUTH_USER_MODEL = "users.UserModel"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "utils.middleware.CorsMiddleware",  # 允许所有跨域，仅在测试环境使用（自定义的中间件)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Mysql数据库配置
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "demo",
        'USER': 'root',
        'PASSWORD': "123456",
        'HOST': "127.0.0.1",
        'OPTIONS': { 'init_command': 'SET storage_engine=INNODB;' }  # 这里如果报错storage_engine就改成 default_storage_engine
        # 'OPTIONS': { 'init_command': 'SET default_storage_engine=INNODB;' }  # 这里如果报错storage_engine就改成 default_storage_engine
    }
}
# 注意新建mysql数据库，字符选择 utf-8 Unicode，排序选 utf8_general_ci
"""

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'  # 中文

TIME_ZONE = 'Asia/Shanghai'  # 时区为上海

USE_I18N = True  # 加载国际化支持机制

USE_TZ = False  # 数据库中使用本地时间

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
