from django.shortcuts import render
from .models import ArticleModel
from .serializers import ArticleSerializer
from rest_framework import viewsets
from utils.permissions import IsOwnerOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(description='查询文章列表'),
    create=extend_schema(description='新增一个文章信息'),
    retrieve=extend_schema(description='查询某个文章内容'),
    update=extend_schema(description='更新某个文章内容'),
    partial_update=extend_schema(description='部分更新某个文章内容'),
    destroy=extend_schema(description='删除某个文章'),
)
class ArticleViewSet(viewsets.ModelViewSet):
    """
    ## 文章管理
    """
    queryset = ArticleModel.objects.all()  # 这里并没有真的取数据，只是生成一个sql语句
    serializer_class = ArticleSerializer
    permission_classes = (IsOwnerOrReadOnly, )
