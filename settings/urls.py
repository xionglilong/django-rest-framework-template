"""settings URL Configuration
rdf官方教程:
    https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/
rdf API指南:
    https://www.django-rest-framework.org/api-guide/routers/
django中文文档:
    https://docs.djangoproject.com/zh-hans/4.0/topics/http/urls/


Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from persons.views import PersonListViewSet
from users.views import SmsCodeViewSet, UserViewSet
from articles.views import ArticleViewSet


router = DefaultRouter()
# 自动绑定ViewSet的方法，自动配置路由
router.register(r'persons', PersonListViewSet, basename='persons')  # 人员信息收集
router.register(r'codes', SmsCodeViewSet, basename='codes')  # 短信验证码
router.register(r'users', UserViewSet, basename='users')  # 用户注册、查询个人信息
router.register(r'articles', ArticleViewSet, basename='articles')   # 文章

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # 调试api的认证接口，可浏览的API的登录和注销视图，配置了才会在可浏览api界面出现登录按钮

    # 配置jwt认证接口（djangorestframework-simplejwt)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 接受json认证：{"username": "xiongda", "password": "123456"}
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # 自动生成api文档（drf-spectacular）
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # swagger接口文档
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # redoc接口文档



]
