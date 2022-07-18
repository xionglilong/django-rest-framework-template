from django.contrib import admin
from .models import PersonModel, FamilyModel
from settings.admin import GenericModelAdminClass


@admin.register(PersonModel)
class PersonAdmin(admin.ModelAdmin, metaclass=GenericModelAdminClass):
    model = PersonModel
    # ------------------------------------ 列表页配置 ------------------------------------
    search_fields = ('name', 'mobile')  # 列表页搜索功能的查询范围
    list_filter = ('sex', 'age')  # 列表过滤器的字段

    readonly_fields = ('owner', )  # 详情页中只读字段


@admin.register(FamilyModel)
class FamilyAdmin(admin.ModelAdmin, metaclass=GenericModelAdminClass):
    model = FamilyModel
    # ------------------------------------ 列表页配置 ------------------------------------
    search_fields = ('name', 'mobile')  # 列表页搜索功能的查询范围
    list_filter = ('relation',)  # 列表过滤器的字段
    date_hierarchy = 'create_time'  # 列表页时间过滤器的字段
