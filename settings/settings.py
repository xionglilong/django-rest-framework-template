"""
版本 Django 4.0.6.
文档：https://docs.djangoproject.com/en/4.0/topics/settings/
文档：https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import sys
from pathlib import Path
from datetime import timedelta



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
    'django.contrib.admin',  # 管理站点后台功能
    'django.contrib.auth',  # 包含了验证框架的内核和它的默认模型
    'django.contrib.contenttypes',  # 允许你创建的模型和权限相关联
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # 静态文件管理
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',  # 添加过滤器包 (django-filter)
    'drf_spectacular',  # 自动生成api文档
    'tinymce',  # 后台管理富文本小部件 (django-tinymce)
    'mptt',  # 树状模型 (django-mptt)
    'django_mptt_admin',  # 树状模型后台管理页面 (django-mptt-admin)
    'users.apps.UsersConfig',  # app: 自定义用户登录注册
    'persons.apps.PersonsConfig',  # app: 人员信息搜集
    'articles.apps.ArticlesConfig',  # app: 新闻文章
    'goods.apps.GoodsConfig',  # app: 商品
]

# rest_framework的全局配置
REST_FRAMEWORK = {
    # 分页功能的全局设置
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # 修改默认的分页类型，使用每页数量和页面编号来分页
    'PAGE_SIZE': 20,  # 每个页面的数量，配置完后立马有分页功能，并且json数据格式会调整，还会多出几个字段：count、next、previous，文件路径字段还会添加完整域名

    'DEFAULT_AUTHENTICATION_CLASSES': (  # 允许的认证方式(全局开启)。类似于中间件，按顺序执行authenticate()，主要是通过不同的认证方式来查找用户并设置request.user
        'rest_framework.authentication.BasicAuthentication',  # 浏览器弹框认证
        'rest_framework.authentication.SessionAuthentication',  # 依赖django的SessionMiddleware、AuthenticationMiddleware，一般浏览器常见，前后端分离一般不用，不过内置文档功能要用
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',  # 这个不建议全局配置，建议在ViewSet单独配置，因为如果传过来的token过期了会报错，可能导致公共数据查询失败
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # drf-spectacular api文档配置
}

# drf-spectacular api文档配置: https://github.com/tfranzel/drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': '项目API接口文档',
    'DESCRIPTION': '项目详情介绍',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

# drf-extensions 缓存配置
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 2,  # 缓存时间为2秒
}


# djangorestframework-simplejwt 用户登录认证配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),  # token过期时间
    'AUTH_HEADER_TYPES': ('Bearer', 'token'),  # header头部的内容开头标记
}

# admin富文本编辑器
TINYMCE_DEFAULT_CONFIG = {
    # 'mode': 'textareas',
    # 'theme': 'advanced',  # 这个主题没有js文件
    'width': 800,
    'height': 600,
    'theme': 'silver',  # 主题
    'language': 'zh_CN',  # 中文
    'menubar': 'edit format',  # 菜单栏
    'plugins': 'lists,advlist bold underline alignleft aligncenter alignright fontselect fontsizeselect code image link table',
    'toolbar': 'bullist numlist bold underline alignleft aligncenter alignright fontselect fontsizeselect code image link table',
    'images_upload_url': '/uploading/',   # 图片上传处理视图
    'style_formats': [
        {'title': 'Bold text', 'inline': 'b'},
        {'title': 'Red text', 'inline': 'span', 'styles': {'color': '#ff0000'}},
        {'title': 'Red header', 'block': 'h1', 'styles': {'color': '#ff0000'}},
        {'title': 'Example 1', 'inline': 'span', 'classes': 'example1'},
        {'title': 'Example 2', 'inline': 'span', 'classes': 'example2'},
        {'title': 'Table styles'},
        {'title': 'Table row 1', 'selector': 'tr', 'classes': 'tablerow1'}
    ]
}


# 自定义用户模型
AUTH_USER_MODEL = 'users.UserModel'

# 自定义登录
# AUTHENTICATION_BACKENDS = (
#     'users.views.CustomAuthenticationBackend',
# )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # 通过请求管理 sessions
    "utils.middleware.CorsMiddleware",  # 允许所有跨域，仅在测试环境使用（自定义的中间件)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 使用会话将用户和请求关联
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

# django-redis: Redis 配置 （django默认使用本地内存，重启后缓存内容失效）
"""
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://password@127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
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
# DATETIME_FORMAT = 'Y-m-d H:i:s'  # 加载国际化支持后，这两个参数会被覆盖，就注释掉
# DATE_FORMAT = 'Y-m-d'

USE_TZ = False  # 数据库中使用本地时间

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)  # 静态文件自动搜索路径（自动管理，无须配置url即可访问）
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # 静态文件存储路径（手动管理，需要在urls.py中手动配置）

# 媒体资源路径（drf会自动修改媒体文件url路径）
MEDIA_URL = '/media/'  # 路径形式
# MEDIA_URL = 'https://www.example.com/media/'  # 链接形式
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 手动管理媒体文件

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
