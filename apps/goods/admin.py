from django.contrib import admin
from .models import GoodCategoryModel, GoodModel, ShoppingCartModel, OrderInfoModel, OrderGoodModel


@admin.register(GoodCategoryModel)
class GoodCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(GoodModel)
class GoodAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCartModel)
class ShoppingCartModel(admin.ModelAdmin):
    pass


@admin.register(OrderInfoModel)
class OrderInfoModelAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderGoodModel)
class OrderGoodAdmin(admin.ModelAdmin):
    pass
