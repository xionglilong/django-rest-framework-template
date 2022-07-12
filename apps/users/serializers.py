from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserModel
from persons.models import PersonModel


class UserSerializer(serializers.ModelSerializer):
    # person在用户模型中是反向关联关系，不会默认包含，需要手动添加显式字段
    persons = serializers.PrimaryKeyRelatedField(many=True, queryset=PersonModel.objects.all())

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'persons')
