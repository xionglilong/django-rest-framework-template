from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import ArticleModel, ArticleTagModel


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleModel
        fields = "__all__"  # 这里是映射模型的所有字段


class ArticleTagSerializer(serializers.ModelSerializer):
    """文章标签 序列化器"""
    class Meta:
        model = ArticleTagModel
        fields = '__all__'
        # 定制一个验证器。其实数据模型表中已经配置好了，模型序列化器可以自动读取，可是报错信息没有体验，所以这里重复配置一下
        validators = [
            UniqueTogetherValidator(queryset=ArticleModel.objects.all(), fields=('owner', 'name'), message='标签重复')
        ]
