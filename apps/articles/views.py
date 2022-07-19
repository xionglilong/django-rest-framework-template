# Generic views: https://www.django-rest-framework.org/api-guide/generic-views/

from django.shortcuts import render
import os
from django.http import JsonResponse
from django.conf import settings
from .models import ArticleModel
from .serializers import ArticleSerializer, ArticleTagSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from utils.permissions import IsOwnerOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.authentication import JWTAuthentication


class ArticleViewSet(viewsets.ModelViewSet):
    """
    ## 文章管理
    """
    # queryset = ArticleModel.objects.all()  # 因为下面有get_queryset()，所以不需要就注释掉。这里并没有真的取数据，只是生成一个sql语句
    serializer_class = ArticleSerializer
    permission_classes = (IsOwnerOrReadOnly, )  # 自己可写，匿名仅可读

    # 重载，不用上面的queryset属性。功能：自己文章只有自己能看到
    def get_queryset(self):
        return ArticleModel.objects.filter(owner=self.request.user)

    class Meta:
        tags = ['文章']


class ArticleTagViewSet(viewsets.ModelViewSet):
    """
    ## 文章标签管理
    """
    serializer_class = ArticleTagSerializer
    authentication_classes = (JWTAuthentication, SessionAuthentication)  # 允许的认证方式，使用JWT认证和session会话认证。session主要用来浏览器测试。(这里会覆盖全局配置)
    # 权限：首先必须得登录，其次必须自己才能写
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )

    # lookup_field = 'name'  # 获取url的id参数后，默认是搜索主键，特殊情况下，这里可以自定义一个键

    # 重载，不用queryset属性。功能：自己文章只有自己能看到
    def get_queryset(self):
        return ArticleModel.objects.filter(owner=self.request.user)

    class Meta:
        tags = ['文章标签']


# 文章图片上传
@csrf_exempt
def uploading(request):
    img_obj = request.FILES.get('file')
    file_url = os.path.join(settings.MEDIA_ROOT, img_obj.name)
    with open(file_url, "wb") as file:
        data = img_obj.file.read()
        file.write(data)
    return JsonResponse({
        "location": '/media/' + img_obj.name
    })
