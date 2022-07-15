# serializers: https://www.django-rest-framework.org/api-guide/serializers/
# serializer field: https://www.django-rest-framework.org/api-guide/fields/
# Validators: https://www.django-rest-framework.org/api-guide/validators/


import re
import string
import random
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from persons.models import PersonModel
from .models import SmsCodeModel
from rest_framework.validators import UniqueValidator
from utils.send_sms import AliyunSendSMS


UserModel = get_user_model()


# 用户注册数据序列化器
class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    # person在用户模型中是反向关联关系，不会默认包含，需要手动添加显式字段
    # persons = serializers.PrimaryKeyRelatedField(many=True, queryset=PersonModel.objects.all())  # 本身没有这个字段，关联自己的外键的表
    username = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[UniqueValidator(queryset=UserModel.objects.all(), message="用户已经存在")], label="用户名", help_text="请输入用户名")
    password = serializers.CharField(write_only=True, allow_blank=True, style={'input_type': 'password'}, label='密码')
    code = serializers.CharField(required=True, max_length=6, min_length=6, help_text="验证码", label="验证码", write_only=True, error_messages={"required": "请输入验证码", "max_length": "验证码要求6位数字", "min_length": "验证码要求6位数字", 'blank': "请输入验证码"})

    # 注册用户时，将保存密文密码 （这个功能使用信号量更方便，所有就注释了代码）
    """
    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)  # 这里返回其实已经保存在数据库中，只是我们再更新数据库的密码字段
        user.set_password(validated_data['password'])
        user.save()
        return user
    """

    def validate_code(self, code):
        result = AliyunSendSMS().validate_code(mobile=self.initial_data['mobile'], code=code)  # initial_data是前端传过来的值
        if not result['success']:
            raise serializers.ValidationError(result['message'])
        return None  # 这个字段只做个验证，不保存到数据库

    def validate_mobile(self, mobile):
        if not re.match(r"^1[358]\d{9}$|^147\d{8}$|^176\d{8}$", mobile):
            raise serializers.ValidationError("非法手机号")
        return mobile

    def validate_password(self, password):
        # 如果没有设置密码，则配置个随机密码
        if not password:
            password = ''.join(random.sample(string.ascii_letters + string.digits, 16))  # 生成16位随机字符，包括大小写字母和数字
        return password


    def validate(self, attrs):
        # attrs 是所有字段都validate_XXX后返回的一个总的验证后的数据
        if not attrs.get('username', None):
            attrs['username'] = attrs['mobile']  # 手动添加 username 字段数据
        del attrs['code']  # 删除code数据，因为不需要保存到数据库。如果不删除，code=None还是会有保存数据库操作

        return attrs

    class Meta:
        model = UserModel
        fields = ('username', 'mobile', 'code', 'password')


# 短信数据序列化器
class SmsSerializer(serializers.Serializer):  # 这里用不了模型序列化器，因为code为必填字段没法及时填写
    """短信序列化器"""
    mobile = serializers.CharField(max_length=11)

    # 验证手机号
    def validate_mobile(self, mobile):
        # 手机号是否已经注册
        if UserModel.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")
        # 手机号是否合法
        if not re.match(r"^1[358]\d{9}$|^147\d{8}$|^176\d{8}$", mobile):
            raise serializers.ValidationError("非法手机号")
        # 发送频率限制
        before_time = datetime.now() - timedelta(hours=0, minutes=0, seconds=50)
        if SmsCodeModel.objects.filter(create_time__gt=before_time, mobile=mobile):
            raise serializers.ValidationError("发送频率过快")
        return mobile

    def create(self, validated_data):  # 如果不用调用save()方法，也可以留空
        pass

    def update(self, instance, validated_data):  # 如果不用调用save()方法，也可以留空
        pass



