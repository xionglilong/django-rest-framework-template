import datetime

from django.db import models
from django.contrib.auth import get_user_model  # UserModel的快捷方式，当然你也可以自己手动导入用户的Model
from utils.app.models import GenericModelClass, GenericModel, OwnerModelClass


UserModel = get_user_model()

SEX_CHOICES = [(1, '男'), (0, '女')]


# 人员信息表
class PersonModel(metaclass=OwnerModelClass):
    # id = models.IntegerField(primary_key=True)  # 手动设置主键，不建议填写，django会自动添加id主键，这里只是手写示例
    name = models.CharField(verbose_name='姓名', max_length=10, help_text="姓名")
    sex = models.BooleanField('性别', choices=SEX_CHOICES, help_text="性别")
    age = models.IntegerField('年龄', blank=True, null=True, help_text="年龄")
    email = models.EmailField('邮箱', blank=True, help_text="邮箱")
    phone = models.CharField('电话', max_length=11, help_text="电话", unique=True)
    description = models.TextField('人员其他详细信息', help_text="人气其他详细信息")
    icon = models.ImageField('头像', upload_to="head/", blank=True, default='', help_text="头像")

    class Meta:
        verbose_name = "人员信息表"
        verbose_name_plural = verbose_name  # 后台admin中，复数形式展示

    # 如果需要处理保存前的模型数据，重写save()，这里只是示例
    def save(self, *args, **kwargs):
        self.phone = self.phone and '+86' + self.phone or ''
        super().save(*args, **kwargs)


# --------------自定义管理器-----------------
# 这里仅作为了解
class FamilyManager(models.Manager):
    def number_count(self, keyword):
        return self.filter(number=keyword).count()


# ----------------------------------------

RELATION_CHOICES = [('父亲', '父亲'), ('母亲', '母亲'), ('姐姐', '姐姐'), ('妹妹', '妹妹'), ('哥哥', '哥哥'), ('弟弟', '弟弟')]


# 家庭成员表
class FamilyModel(metaclass=GenericModelClass):
    name = models.CharField(verbose_name='姓名', max_length=10, help_text="姓名")
    objects = FamilyManager()  # 加载自定义的管理器
    relation = models.CharField('关系', max_length=10, choices=RELATION_CHOICES, help_text="关系")
    mobile = models.CharField('电话', max_length=20, blank=True, default='', help_text="电话")

    # 外键,数据库键名:person_id,关联到了Person表id键
    # 可以通过关联名related_name反向查询子表的数据，当然也可以通过"小写的子表名_set"的形式代替
    person = models.ForeignKey(PersonModel, on_delete=models.CASCADE, related_name='families', help_text="所属人", verbose_name='所属人')

    class Meta:
        verbose_name = "家庭成员"
        verbose_name_plural = verbose_name  # 后台admin中，复数形式展示

