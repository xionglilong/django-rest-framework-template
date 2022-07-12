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
    'corsheaders',
    'persons.apps.PersonsConfig',
    'users.apps.UsersConfig',
]

# rest_framework的全局配置
REST_FRAMEWORK = {
    # 分页功能的全局设置
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # 修改默认的分页类型，使用每页数量和页面编号来分页
    'PAGE_SIZE': 20,  # 每个页面的数量，配置完后立马有分页功能，并且json数据格式会调整，还会多出几个字段：count、next、previous，文件路径字段还会添加完整域名

}

# 自定义用户模型
AUTH_USER_MODEL = "users.UserModel"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "utils.middleware.CorsMiddleware",  # 允许所有跨域，（自定义的中间件)
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
        'DIRS': [],
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
