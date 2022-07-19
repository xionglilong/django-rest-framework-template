"""
    这里存放用户相关模型数据表，请不要在这里导入自定义的模型基类模块，会造成模块导入的死循环报错
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from mptt.models import MPTTModel, TreeForeignKey

SEX_CHOICES = [(1, '男'), (0, '女')]


# 扩展内置的user表（内置字段有：first_name,last_name,username,password,email,is_superuser,is_active,is_joined,date_joined,last_login）
# 注意：关联了信号量，请查看signals.py文件
class UserModel(AbstractUser):
    name = models.CharField(verbose_name="姓名", max_length=50, default="", help_text="请输入您的姓名或昵称")
    birthday = models.DateField("生日", null=True, blank=True, help_text="生日")
    sex = models.BooleanField('性别', choices=SEX_CHOICES, default=1, help_text="性别", blank=True)
    address = models.CharField("住址", max_length=100, default="", help_text="住址", blank=True)
    mobile = models.CharField("手机号", max_length=11, help_text="请输入11位的手机号", default='')
    icon = models.ImageField("头像路径", upload_to="head/%Y/%m", default="head/default.png", max_length=100, help_text="头像路径", blank=True)
    handover_id = models.IntegerField('数据交接人', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name
        db_table = "auth_user"  # 自定表名(选填，不过这里建议还是这么写。默认表名为：app名_模型名小写)
        ordering = ('-update_time',)

    def __str__(self):
        return self.name


# 部门表
class DepartmentModel(MPTTModel):
    name = models.CharField('部门名称', max_length=128, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='父级部门')
    # 因为元类不同所以不能使用元类，重写一下时间字段，把时间字段放在后面
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "部门管理"
        verbose_name_plural = verbose_name
        db_table = "auth_department"  # 自定表名
        ordering = ('-update_time',)

    def __str__(self):
        return self.name


# 短信验证码表
class SmsCodeModel(models.Model):
    mobile = models.CharField('手机号', max_length=11)
    code = models.CharField('验证码', max_length=4)
    used = models.BooleanField('是否被使用', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.mobile + '：' + self.code

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name
        ordering = ('-update_time',)
