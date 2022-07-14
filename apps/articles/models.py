# https://blog.csdn.net/qq_42778001/article/details/111768991
# https://zhuanlan.zhihu.com/p/79573405
# https://www.liujiangblog.com/course/django/98
# https://www.jb51.net/article/167289.htm

from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


# 文章标签
class ArticleTagModel(models.Model):
    name = models.CharField('标签名称', max_length=20)
    owner = models.ForeignKey(UserModel, related_name='article_tag', on_delete=models.CASCADE, verbose_name='创建人', help_text="创建人")  # 把数据外键关联到一个所有者
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = "文章标签表"
        verbose_name_plural = verbose_name
        ordering = ('create_time', )
        unique_together = ("name", "owner")  # 联合唯一约束

    def __str__(self):  # 在后台admin列表中显示的字段
        return self.name  # 这里填入的字段的数据内容不要为空


# 文章
class ArticleModel(models.Model):
    title = models.CharField('文章标题', max_length=100, help_text="请输入文章标题")
    content = models.TextField('文章内容', help_text="请输入文章内容")
    tags = models.ManyToManyField(to=ArticleTagModel, related_name="tags", blank=True, default=None, verbose_name='标签', help_text="请选择一些标签")
    owner = models.ForeignKey(UserModel, related_name='article', on_delete=models.CASCADE, verbose_name='创建人')  # 把数据外键关联到一个所有者
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = "文章表"
        verbose_name_plural = verbose_name
        ordering = ('create_time', )

    def __str__(self):  # 在后台admin列表中显示的字段
        return self.title + " —— " + self.owner.nick_name  # 这里填入的字段的数据内容不要为空
