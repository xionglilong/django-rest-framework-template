import random
import re
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import SmsSerializer, UserRegisterSerializer, UserDetailSerializer
from utils.send_sms import AliyunSendSMS  # 发送验证码函数
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_simplejwt.authentication import JWTAuthentication

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


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """
    ## 用户注册
    """
    serializer_class = UserRegisterSerializer
    queryset = UserModel.objects.all()
    authentication_classes = (JWTAuthentication, authentication.SessionAuthentication)  # session认证是浏览器调试使用

    # post请求
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

    # 动态获取序列化器，替换 serializer_class 属性
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        if self.action == 'retrieve':
            return UserDetailSerializer

    # get请求某个数据模型，delete请求都会用到
    def get_object(self):
        return self.request.user  # 用户随机传递URl的id参数都可以返回自己

    # 权限的动态获取，替换 permission_classes 属性
    def get_permissions(self):
        if self.action == 'retrieve':
            return permissions.IsAuthenticated(),  # 如果是查询某个具体信息
        elif self.action == 'create':
            return ()
        return []  # 返回默认值空，需要带上别忘了




