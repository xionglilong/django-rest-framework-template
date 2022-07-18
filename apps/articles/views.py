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


@extend_schema_view(
    list=extend_schema(tags=['文章管理'], operation_id='查看列表', description='查询文章列表'),
    create=extend_schema(tags=['文章管理'], operation_id='创建文章', description='新增一个文章信息'),
    retrieve=extend_schema(tags=['文章管理'], operation_id='文章详情', description='查询某个文章内容'),
    update=extend_schema(tags=['文章管理'], operation_id='更新文章', description='更新某个文章内容'),
    partial_update=extend_schema(tags=['文章管理'], operation_id='部分更新', description='部分更新某个文章字段'),
    destroy=extend_schema(tags=['文章管理'], operation_id='删除文章', description='删除某个文章'),
)
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


@extend_schema_view(
    list=extend_schema(tags=['文章标签管理'], operation_id='查看标签列表', description='查询文章列表'),
    create=extend_schema(tags=['文章标签管理'], operation_id='创建标签', description='新增一个标签信息'),
    retrieve=extend_schema(tags=['文章标签管理'], operation_id='标签详情', description='查询某个标签内容'),
    update=extend_schema(tags=['文章标签管理'], operation_id='更新标签', description='更新某个标签'),
    partial_update=extend_schema(tags=['文章标签管理'], operation_id='部分字段更新', description='部分更新某个标签字段'),
    destroy=extend_schema(tags=['文章标签管理'], operation_id='删除标签', description='删除某个标签'),
)
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
