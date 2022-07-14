from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PersonSerializer
from persons.models import PersonModel
from rest_framework import mixins
from persons.serializers import PersonModel
# from persons.permissions import IsOwnerOrReadOnly
from rest_framework_extensions.cache.mixins import CacheResponseMixin  # 缓存
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(description='列出人员信息列表'),
)
class PersonListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    ## 人员列表
    """
    queryset = PersonModel.objects.all()  # 这里并没有真的取数据，只是生成一个sql语句
    serializer_class = PersonSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    # ------如何使用过滤、搜索、排序？-------
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)  # 添加过滤器功能
    filter_fields = ('age', 'sex')  # 过滤器选项配置
    search_fields = ('name', 'email')  # 搜索选项配置
    ordering_fields = ('age', 'create_time')  # 排序选项配置

    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # 请注意这个函数与上面的queryset属性的功能是一样的，只是这里可以更多的定制，两者选一即可
    # def get_queryset(self):
    #    queryset = PersonModel.objects.all()
    #    age_min = self.request.query_params.get('age_min', 0)
    #    return queryset.filter(age__gt=int(age_min))  # 自定义一个过滤选项，这里只是演示功能，不建议这么使用过滤，太麻烦


# 这里是手动绑定http请求和操作数据的模型Mixin方法（跟之前的在视图类里面的绑定有点像），然后直接放到urls.py里面的path()里面的视图参数里面
# 也可以在urls.py用路由器router对象自动绑定默认行为和注册url，这样更方便。
# person_list = PersonListViewSet.as_view({
#     'get': 'list',
# })
