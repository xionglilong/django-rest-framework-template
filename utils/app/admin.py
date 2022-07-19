# https://www.cnblogs.com/yoyoketang/p/10345793.html
from django.contrib import admin
from django.db import models
from django.contrib.auth import get_user_model
from tinymce.widgets import AdminTinyMCE
from django import forms
UserModel = get_user_model()


class GenericModelAdminClass(forms.MediaDefiningClass):
    """
    通用管理页面元类
        基本上所有的管理页面都可以使用这个元类，它仅仅是做了一些优化的默认配置
    注意：
        在使用时，需要在类中声明 model 属性，用于查找模型
    """

    def __new__(mcs, name, bases, attrs):
        if 'model' not in attrs:
            raise NotImplementedError('必须声明类属性：`model` .')
        else:
            model = attrs['model']

        # ------------------------------------ 列表页配置 ------------------------------------
        # 列表页需要显示的字段（除了反向关联字段、多对多字段、id字段不显示）
        attrs.setdefault('list_display', [field.name for field in model._meta.get_fields() if not field.one_to_many and not field.many_to_many and field.name != 'id'])
        # 列表页搜索功能的查询范围（仅查询CharField字段）
        attrs.setdefault('search_fields', [field.name for field in model._meta.get_fields() if isinstance(field, models.CharField)])
        # 列表过滤器的字段（仅有choices属性字段和布尔字段）
        attrs.setdefault('list_filter', [field.name for field in model._meta.get_fields() if getattr(field, 'choices', None) or isinstance(field, (models.BooleanField, models.NullBooleanField))])
        # 列表页时间过滤器的字段（创建时间选择）
        attrs.setdefault('date_hierarchy', 'create_time')
        # attrs.setdefault('list_display_links', ('name',))  # 可点击进入详情的字段(默认值是第一个)
        # attrs.setdefault('list_editable', ('name',))  # 可直接在列表页修改的字段
        # attrs.setdefault('list_select_related', ('owner',))  # 外键或一对一字段，检索管理变更列表页的对象列表时使用 select_related()。这样可以省去一堆数据库查询。

        # ------------------------------------ 详情页配置 -------------------------------------
        # attrs.setdefault('fields', ('', ''))  # 详情页面中显示的字段和顺序
        # attrs.setdefault('exclude', ('owner',))  # 详情页面排除的字段
        # attrs.setdefault('readonly_fields', ('owner', ))  # 详情页中只读字段
        # attrs.setdefault('fk_fields', ('',))  # 显示外键字段

        # ------------------------------------ 自动优化配置 -----------------------------------
        # 有choices属性的字段以单选按钮显示
        attrs.setdefault('radio_fields', {field.name: admin.HORIZONTAL for field in model._meta.get_fields() if getattr(field, 'choices', None)})
        # 每页显示多少条，默认100条
        attrs.setdefault('list_per_page', 100)
        # 详情页，外键字段(many_to_one)可搜索自动填入
        attrs.setdefault('autocomplete_fields', [field.name for field in model._meta.get_fields() if field.many_to_one])
        # 详情页，多对多(many_to_many)字段选择器优化
        attrs.setdefault('filter_horizontal', [field.name for field in model._meta.get_fields() if field.many_to_many])
        # 详情页，models.TextField字段设置富文本控件
        attrs.setdefault('formfield_overrides', {models.TextField: {'widget': AdminTinyMCE}})

        # 注意：反向关联外键标识为 field.one_to_many == True

        new_class = super().__new__(mcs, name, bases, attrs)
        return new_class


class OwnerModelAdmin(admin.ModelAdmin):
    """
    用户自有资源管理页面
        页面的所有内容都是用户自己的，看不到别人的
    注意：
        在使用时，请不要将 owner 表单字段设置为只读，只读是字符串显示而不是控件显示，不属于表单字段
    """

    # 查询时，普通用户只能看到自己的
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(owner=request.user)

    # 进入增加或修改页面会被调用来获取表单
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=None, change=False, **kwargs)

        # 创建页面中，显示创建人为自己，并且不可选择
        owner_field = form.base_fields.get('owner')
        if owner_field:
            owner_field.disabled = True
            owner_field.initial = request.user
        return form

    # 获取外键字段的表单字段（用于过滤单选按钮内容）
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        # 如果该外键字段的反向关联表中有 owner 字段
        if hasattr(db_field.remote_field, 'owner'):
            # 那么只能查到自己创建的选项
            field.queryset = db_field.related_model.objects.filter(owner=request.user)
        return field

    # 获取多对多字段的表单字段（用于过滤多选按钮内容）
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        field = super().formfield_for_manytomany(db_field, request, **kwargs)
        # 如果反向关联的表中有 owner 字段
        if hasattr(db_field.remote_field, 'owner'):
            # 那么只能查到自己创建的选项
            field.queryset = db_field.related_model.objects.filter(owner=request.user)
        return field

    # 数据创建或修改操作时
    def save_model(self, request, obj, form, change):
        if not change:  # 如果是创建操作，而不是修改操作
            obj.owner = request.user  # 将文章外键关联为自己
        super().save_model(request, obj, form, change)
