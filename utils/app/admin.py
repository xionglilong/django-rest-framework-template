# https://www.cnblogs.com/yoyoketang/p/10345793.html
from django.contrib import admin
from django.db import models
from django.contrib.auth import get_user_model
from tinymce.widgets import AdminTinyMCE
from django import forms
UserModel = get_user_model()


class GenericModelAdminClass(forms.MediaDefiningClass):
    """
    自定义元类
    """

    def __new__(mcs, name, bases, attrs):
        if 'model' not in attrs:
            raise NotImplementedError('必须声明类属性：`model` .')
        else:
            model = attrs['model']

        # ------------------------------------ 列表页配置 ------------------------------------
        # 列表页需要显示的字段
        attrs.setdefault('list_display', [field.name for field in model._meta.get_fields() if not field.one_to_many and not field.many_to_many and field.name != 'id'])
        # 列表页搜索功能的查询范围
        attrs.setdefault('search_fields', [field.name for field in model._meta.get_fields() if isinstance(field, models.CharField)])
        # 列表过滤器的字段
        attrs.setdefault('list_filter', [field.name for field in model._meta.get_fields() if getattr(field, 'choices', None) or isinstance(field, (models.BooleanField, models.NullBooleanField))])
        # 列表页时间过滤器的字段
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
