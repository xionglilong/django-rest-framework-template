import random
import re
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import SmsSerializer, UserRegisterSerializer
from .models import SmsCodeModel
from utils.send_sms import AliyunSendSMS  # 发送验证码函数
from rest_framework_simplejwt.tokens import RefreshToken

UserModel = get_user_model()


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username=username) | Q(mobile=username))
            # 密码登录验证
            if password and user.check_password(password):
                return user
            # 短信登录验证
            if re.match(r"^\d{6}$", password) and re.match(r"^1[358]\d{9}$|^147\d{8}$|^176\d{8}$", username) and AliyunSendSMS().validate_code(password)['success']:
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    ## 发送短信验证码
    """

    serializer_class = SmsSerializer

    # @extend_schema( description="", )
    def create(self, request, *args, **kwargs):
        """## 发送验证码"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 如果数据验证没通过直接抛出异常，会被drf捕获返回400响应，不执行后面语句

        mobile = serializer.validated_data["mobile"]
        # 发送验证码
        result = AliyunSendSMS().send_code(mobile)
        if result['success']:
            return Response({"mobile": mobile}, status=status.HTTP_201_CREATED)
        else:  # 如果发送失败
            return Response({"mobile": result["message"]}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    ## 用户注册
    """
    serializer_class = UserRegisterSerializer
    queryset = UserModel.objects.all()

    def create(self, request, *args, **kwargs):
        """## 创建一个新用户"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # 创建用户后，返回登录token
        result_dict = serializer.data
        refresh = RefreshToken.for_user(user)
        result_dict['access'] = str(refresh.access_token)
        result_dict['refresh'] = str(refresh)

        headers = self.get_success_headers(serializer.data)
        return Response(result_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


