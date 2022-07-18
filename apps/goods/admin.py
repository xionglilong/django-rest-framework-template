from django.contrib import admin
from django.db import models
from .models import GoodCategoryModel, GoodModel, ShoppingCartModel, OrderInfoModel, OrderGoodModel
from tinymce.widgets import AdminTinyMCE
from settings.admin import GenericModelAdminClass


@admin.register(GoodCategoryModel)
class GoodCategoryAdmin(admin.ModelAdmin, metaclass=GenericModelAdminClass):
    model = GoodCategoryModel
    # ------------------------------------ 列表页配置 ------------------------------------
    list_display = [field.name for field in GoodCategoryModel._meta.get_fields() if not field.one_to_many and not field.many_to_many and field.name != 'id']  # 列表页需要显示的字段
    search_fields = ('name', 'code', 'desc')  # 列表页搜索功能的查询范围
    list_filter = ('category_type', 'is_tab')  # 列表过滤器的字段
    date_hierarchy = 'create_time'  # 列表页时间过滤器的字段


@admin.register(GoodModel)
class GoodAdmin(admin.ModelAdmin, metaclass=GenericModelAdminClass):
    model = GoodModel
    # ------------------------------------ 列表页配置 ------------------------------------
    search_fields = ('good_sn', 'name', 'brief_desc', 'desc')  # 列表页搜索功能的查询范围
    list_filter = ('category', 'is_new', 'is_hot')  # 列表过滤器的字段
    readonly_fields = ('click_num', 'fav_num')  # 详情页中只读字段


@admin.register(ShoppingCartModel)
class ShoppingCartModel(admin.ModelAdmin, metaclass=GenericModelAdminClass):
    model = ShoppingCartModel
    # ------------------------------------ 列表页配置 ------------------------------------
    list_display = [field.name for field in ShoppingCartModel._meta.get_fields() if not field.one_to_many and not field.many_to_many and field.name != 'id']  # 列表页需要显示的字段
    search_fields = ('owner', 'good')  # 列表页搜索功能的查询范围


@admin.register(OrderInfoModel)
class OrderInfoModelAdmin(admin.ModelAdmin, metaclass=GenericModelAdminClass):
    model = OrderInfoModel
    # ------------------------------------ 列表页配置 ------------------------------------
    search_fields = ('owner', 'order_sn', 'trade_no')  # 列表页搜索功能的查询范围
    list_filter = ('pay_status', )  # 列表过滤器的字段
    date_hierarchy = 'create_time'  # 列表页时间过滤器的字段
    readonly_fields = ('pay_status', 'order_sn', 'trade_no', 'owner', 'price_count')  # 详情页中只读字段



@admin.register(OrderGoodModel)
class OrderGoodAdmin(admin.ModelAdmin, metaclass=GenericModelAdminClass):
    model = OrderGoodModel
    # ------------------------------------ 列表页配置 ------------------------------------
    search_fields = ('order', )  # 列表页搜索功能的查询范围
    date_hierarchy = 'create_time'  # 列表页时间过滤器的字段
    readonly_fields = ('order', 'good', 'num')  # 详情页中只读字段
