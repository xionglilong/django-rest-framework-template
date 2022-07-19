# https://www.cnblogs.com/yoyoketang/p/10345793.html
from typing import Type

from django.contrib import admin
from utils.app.admin import GenericModelAdminClass, OwnerModelAdmin
from .models import ArticleModel, ArticleTagModel
from django.db import models
from django.contrib.auth import get_user_model
from tinymce.widgets import AdminTinyMCE
UserModel = get_user_model()


@admin.register(ArticleModel)
class ArticleAdmin(OwnerModelAdmin, metaclass=GenericModelAdminClass):
    model = ArticleModel


@admin.register(ArticleTagModel)
class ArticleTagAdmin(OwnerModelAdmin, metaclass=GenericModelAdminClass):
    model = ArticleTagModel
