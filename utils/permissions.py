# https://www.django-rest-framework.org/api-guide/permissions/
from rest_framework import permissions


# 匿名可读，属于自己的可写
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):  # obj: 数据库取出来的model
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
