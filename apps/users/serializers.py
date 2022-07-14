import re
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from persons.models import PersonModel
from .models import SmsCodeModel
from rest_framework.validators import UniqueValidator


UserModel = get_user_model()


# 用户注册序列化器
class UserRegisterSerializer(serializers.ModelSerializer):
    # person在用户模型中是反向关联关系，不会默认包含，需要手动添加显式字段
    # persons = serializers.PrimaryKeyRelatedField(many=True, queryset=PersonModel.objects.all())  # 本身没有这个字段，关联自己的外键的表
    username = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[UniqueValidator(queryset=UserModel.objects.all(), message="用户已经存在")], label="用户名", help_text="请输入用户名")
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, label='密码')
    code = serializers.CharField(required=True, max_length=4, min_length=4, help_text="验证码", label="验证码", write_only=True, error_messages={"required": "请输入验证码", "max_length": "验证码要求4位数字", "min_length": "验证码要求4位数字", 'blank': "请输入验证码"})

    # 注册用户时，将保存密文密码 （这个功能使用信号量更方便，所有就注释了代码）
    """
    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)  # 这里返回其实已经保存在数据库中，只是我们再更新数据库的密码字段
        user.set_password(validated_data['password'])
        user.save()
        return user
    """


    def validate_code(self, code):
        code_queryset = SmsCodeModel.objects.filter(mobile=self.initial_data['mobile']).order_by('-create_time')  # initial_data是前端传过来的值
        if code_queryset:
            last_code = code_queryset[0]  # 只取数据库最近的一条
            before_time = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)  # 有效期5分钟
            if before_time > last_code.create_time:
                raise serializers.ValidationError('验证码已过期')
            if last_code.code != code:
                raise serializers.ValidationError('验证码错误')
            return None  # 这个字段只做个验证，不保存到数据库
        else:  # 数据库都没有记录发送过的验证码
            raise serializers.ValidationError('请先发送验证码')

    def validate_mobile(self, mobile):
        if not re.match(r"^1[358]\d{9}$|^147\d{8}$|^176\d{8}$", mobile):
            raise serializers.ValidationError("非法手机号")
        return mobile

    def validate(self, attrs):
        # attrs 是所有字段都validate_XXX后返回的一个总的验证后的数据
        if not attrs.get('username', None):
            attrs['username'] = attrs['mobile']  # 手动添加 username 字段数据
        del attrs['code']  # 删除code数据，因为不需要保存到数据库

        return attrs

    class Meta:
        model = UserModel
        fields = ('username', 'mobile', 'code', 'password')


# 短信序列号器
class SmsSerializer(serializers.Serializer):  # 这里用不了模型序列化器，因为code为必填字段没法及时填写
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
        before_time = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if SmsCodeModel.objects.filter(create_time__gt=before_time, mobile=mobile):
            raise serializers.ValidationError("发送频率过快")
        return mobile

    def create(self, validated_data):  # 如果不用调用save()方法，也可以留空
        pass

    def update(self, instance, validated_data):  # 如果不用调用save()方法，也可以留空
        pass



