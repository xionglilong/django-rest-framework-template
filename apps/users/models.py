from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import AbstractUser


SEX_CHOICES = [(1, '男'), (0, '女')]


# 扩展内置的user表（内置字段有：first_name,last_name,username,password,email,is_superuser,is_active,is_joined,date_joined,last_login）
class UserModel(AbstractUser):
    nick_name = models.CharField(verbose_name="昵称", max_length=50, default="", help_text="昵称")
    birthday = models.DateField("生日", null=True, blank=True, help_text="生日")
    sex = models.BooleanField('性别', choices=SEX_CHOICES, default=1, help_text="性别")
    address = models.CharField("住址", max_length=100, default="", help_text="住址")
    mobile = models.CharField("手机号", max_length=11, null=True, blank=True, help_text="手机号")
    icon = models.ImageField("头像路径", upload_to="head/%Y/%m", default="head/default.png", max_length=100, help_text="头像路径")

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name
        db_table = "auth_user"  # 自定表名(选填，不过这里建议还是这么写。默认表名为：app名_模型名小写)

    def __str__(self):
        return self.nick_name
