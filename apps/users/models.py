from django.db import models

# Create your models here.

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from mptt.models import MPTTModel, TreeForeignKey


SEX_CHOICES = [(1, '男'), (0, '女')]


# 扩展内置的user表（内置字段有：first_name,last_name,username,password,email,is_superuser,is_active,is_joined,date_joined,last_login）
# 注意：关联了信号量，请查看signals.py文件
class UserModel(AbstractUser):
    nickname = models.CharField(verbose_name="昵称", max_length=50, default="", help_text="昵称")
    birthday = models.DateField("生日", null=True, blank=True, help_text="生日")
    sex = models.BooleanField('性别', choices=SEX_CHOICES, default=1, help_text="性别")
    address = models.CharField("住址", max_length=100, default="", help_text="住址")
    mobile = models.CharField("手机号", max_length=11, help_text="请输入11位的手机号")
    icon = models.ImageField("头像路径", upload_to="head/%Y/%m", default="head/default.png", max_length=100, help_text="头像路径")

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name
        db_table = "auth_user"  # 自定表名(选填，不过这里建议还是这么写。默认表名为：app名_模型名小写)

    def __str__(self):
        return self.nickname


# 部门表
class DepartmentModel(MPTTModel):
    name = models.CharField('部门名称', max_length=128, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='父级部门')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "部门管理"
        verbose_name_plural = verbose_name
        db_table = "auth_department"  # 自定表名

    def __str__(self):
        return self.name

# 短信验证码表
class SmsCodeModel(models.Model):
    mobile = models.CharField('手机号', max_length=11)
    code = models.CharField('验证码', max_length=4)
    used = models.BooleanField('是否被使用', default=0)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
