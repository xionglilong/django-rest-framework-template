# https://github.com/mbraak/django-mptt-admin

from django.contrib import admin
# from mptt.admin import MPTTModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import UserModel, DepartmentModel, SmsCodeModel


# 用户管理
@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'nickname')


# 部门管理
@admin.register(DepartmentModel)
class DepartmentAdmin(DjangoMpttAdmin):
    # item_label_field_name = 'name'
    search_fields = ('name', )
    list_filter = ('name',)


@admin.register(SmsCodeModel)
class SmsCodeAdmin(admin.ModelAdmin):
    pass
