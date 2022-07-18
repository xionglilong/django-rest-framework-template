# https://github.com/mbraak/django-mptt-admin

from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import UserModel, DepartmentModel, SmsCodeModel
from utils.app.admin import GenericModelAdminClass


# 用户管理
@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin, metaclass=GenericModelAdminClass):
    model = UserModel
    # ------------------------------------ 列表页配置 ------------------------------------
    search_fields = ('nickname', 'mobile', 'username')  # 列表页搜索功能的查询范围
    list_filter = ('sex',)  # 列表过滤器的字段
    date_hierarchy = 'date_joined'  # 列表页时间过滤器的字段


# 部门管理
@admin.register(DepartmentModel)
class DepartmentAdmin(DjangoMpttAdmin, metaclass=GenericModelAdminClass):
    model = DepartmentModel
    # ------------------------------------ 列表页配置 ------------------------------------
    search_fields = ('name', )  # 列表页搜索功能的查询范围


# 短信验证码管理
@admin.register(SmsCodeModel)
class SmsCodeAdmin(admin.ModelAdmin, metaclass=GenericModelAdminClass):
    model = SmsCodeModel
    # ------------------------------------ 列表页配置 ------------------------------------
    search_fields = ('mobile', 'code')  # 列表页搜索功能的查询范围
