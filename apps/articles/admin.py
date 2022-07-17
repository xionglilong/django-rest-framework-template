from django.contrib import admin
from .models import ArticleModel, ArticleTagModel
from django.db import models
from django.contrib.auth import get_user_model
from tinymce.widgets import AdminTinyMCE
UserModel = get_user_model()


@admin.register(ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    # fields = ()  # 显示字段的顺序
    exclude = ('owner', )  # 不显示的字段
    filter_horizontal = ('tags', )  # 多对多字段选择器优化
    search_fields = ('create_time', )
    autocomplete_fields = ('owner',)  # 外键字段可搜索自动填入
    readonly_fields = ('owner', )  # 只读字段
    formfield_overrides = {models.TextField: {'widget': AdminTinyMCE}}

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
    search_fields = ('name', )

    # 创建或修改时
    def save_model(self, request, obj, form, change):
        if not change:  # 如果是创建操作，而不是修改操作
            obj.owner = request.user  # 将标签外键关联为自己
        super().save_model(request, obj, form, change)

