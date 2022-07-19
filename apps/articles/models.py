# https://blog.csdn.net/qq_42778001/article/details/111768991
# https://zhuanlan.zhihu.com/p/79573405
# https://www.liujiangblog.com/course/django/98
# https://www.jb51.net/article/167289.htm

from django.db import models
from django.contrib.auth import get_user_model
from utils.app.models import GenericModelClass,  get_sentinel_user, GenericModel, OwnerModelClass

UserModel = get_user_model()


# 文章标签
class ArticleTagModel(metaclass=OwnerModelClass):
    name = models.CharField('标签名称', max_length=20)

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name
        unique_together = ("owner", "name")  # 联合唯一约束


# 文章
class ArticleModel(metaclass=OwnerModelClass):
    title = models.CharField('文章标题', max_length=100, help_text="请输入文章标题")
    content = models.TextField('文章内容', help_text="请输入文章内容", default='', blank=True)
    tags = models.ManyToManyField(ArticleTagModel, related_name="tags", blank=True, default=None, verbose_name='标签',
                                  help_text="请选择一些标签")

    class Meta:
        verbose_name = "文章管理"
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)

    def __str__(self):  # 在后台admin列表中显示的字段
        return self.title + " —— " + self.owner.name  # 这里填入的字段的数据内容不要为空
