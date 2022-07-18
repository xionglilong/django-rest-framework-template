from django.contrib import admin
from .models import PersonModel, FamilyModel


@admin.register(PersonModel)
class PersonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PersonModel._meta.get_fields() if field.name not in ('families',)]  # 排除需要显示的字段
    date_hierarchy = 'create_time'  # 时间过滤器的时间字段
    list_editable = ('name', )  # 可直接在列表页修改的字段
    search_fields = ('name',)  # 搜索栏可搜索的字段
    list_filter = ('name', )  # 列表过滤器的字段
    list_select_related = ('owner', )
    # list_display_links = ('owner',)  # 可点击进入详情的字段


@admin.register(FamilyModel)
class FamilyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FamilyModel._meta.get_fields() if field.name not in ()]  # 排除需要显示的字段
    radio_fields = {'person': admin.HORIZONTAL}  # 外键字段以单选按钮显示
