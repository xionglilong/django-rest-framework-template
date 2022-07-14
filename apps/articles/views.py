from django.shortcuts import render
from .models import ArticleModel
from .serializers import ArticleSerializer
from rest_framework import viewsets
from utils.permissions import IsOwnerOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = ArticleModel.objects.all()  # 这里并没有真的取数据，只是生成一个sql语句
    serializer_class = ArticleSerializer
    permission_classes = (IsOwnerOrReadOnly, )
