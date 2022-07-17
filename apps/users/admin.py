from django.contrib import admin
from .models import UserModel, SmsCodeModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'nickname')


@admin.register(SmsCodeModel)
class SmsCodeAdmin(admin.ModelAdmin):
    pass
