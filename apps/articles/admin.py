# https://www.cnblogs.com/yoyoketang/p/10345793.html
from django.contrib import admin
from .models import ArticleModel, ArticleTagModel
from django.db import models
from django.contrib.auth import get_user_model
from tinymce.widgets import AdminTinyMCE
UserModel = get_user_model()


@admin.register(ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    # ------------------------------------ 列表页配置 ------------------------------------
    list_display = [field.name for field in ArticleModel._meta.get_fields() if not field.one_to_many and not field.many_to_many and field.name != 'id']  # 列表页需要显示的字段
    search_fields = ('title', )  # 列表页搜索功能的查询范围
    # list_filter = ('type',)  # 列表过滤器的字段
    date_hierarchy = 'create_time'  # 列表页时间过滤器的字段
    # list_display_links = ('name',)  # 可点击进入详情的字段(默认是第一个)
    # list_editable = ('name',)  # 可直接在列表页修改的字段
    # list_select_related = ('owner',)  # 外键或一对一字段，检索管理变更列表页的对象列表时使用 select_related()。这样可以省去一堆数据库查询。
    # ------------------------------------ 详情页配置 -------------------------------------
    # fields = ('', '')  # 详情页面中显示的字段和顺序
    # exclude = ('owner',)  # 详情页面排除的字段
    readonly_fields = ('owner', )  # 详情页中只读字段
    # fk_fields = ('',)  # 显示外键字段
    # ------------------------------------ 自动优化配置 -----------------------------------

    # 外键字段以单选按钮显示
    # radio_fields = {field.name: admin.HORIZONTAL for field in ArticleModel._meta.get_fields() if field.choices}
    # 每页显示多少条，默认100条
    list_per_page = 100
    # 详情页，外键字段(many_to_one)可搜索自动填入
    autocomplete_fields = [field.name for field in ArticleModel._meta.get_fields() if field.many_to_one]
    # 详情页，多对多(many_to_many)字段选择器优化
    filter_horizontal = [field.name for field in ArticleModel._meta.get_fields() if field.many_to_many]
    # 详情页，models.TextField字段设置富文本控件
    formfield_overrides = {models.TextField: {'widget': AdminTinyMCE}}

    # 注意：反向关联外键标识为 field.one_to_many == True

    # 创建或修改时
    def save_model(self, request, obj, form, change):
        if not change:  # 如果是创建操作，而不是修改操作
            obj.owner = request.user  # 将文章外键关联为自己
        super().save_model(request, obj, form, change)

    # 查询时，普通用户只能看到自己的
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(owner=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # 标签选项，内容只显示自己创建的标签
        if db_field.name == 'tags':
            kwargs['queryset'] = ArticleTagModel.objects.filter(owner=request.user)
        # 创建人选项，内容只显示自己
        if db_field.name == 'owner':
            kwargs['queryset'] = UserModel.objects.filter(pk=request.user.pk)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ArticleTagModel)
class ArticleTagAdmin(admin.ModelAdmin):


    # 创建或修改时
    def save_model(self, request, obj, form, change):
        if not change:  # 如果是创建操作，而不是修改操作
            obj.owner = request.user  # 将标签外键关联为自己
        super().save_model(request, obj, form, change)

