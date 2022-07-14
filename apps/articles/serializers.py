from rest_framework import serializers
from .models import ArticleModel


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleModel
        # fields = ('id', 'name', 'sex', 'age', 'mail', 'phone', 'owner')
        fields = "__all__"  # 这里是映射模型的所有字段
