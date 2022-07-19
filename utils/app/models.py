from django.db import models
from django.db.models.base import ModelBase


class GenericModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True  # 这是一个抽象类，不会迁移到数据库，只为继承使用
        ordering = ('-update_time',)

    # 默认显示第一个字段
    def __str__(self):  # 在后台admin列表中显示的字段
        first_field_name = None
        for field in self._meta.get_fields():
            if field.name != 'id' and not field.many_to_many and not field.one_to_many and not isinstance(field, (models.DateTimeField, models.DateField, models.TimeField)):
                first_field_name = field.name
                break

        if first_field_name:
            return str(getattr(self, first_field_name))
        else:
            return super().__str__()


# 动态生成类，主要解决一个时间字段排序问题，在admin的列表页中，时间字段应该在后面
class GenericModelClass(ModelBase):
    """
    自定义元类
    """

    def __new__(mcs, name, bases, attrs):
        # 如果忘记了继承GenericModel，则添加上去
        if GenericModel not in bases:
            bases = list(bases)
            bases.append(GenericModel)
            bases = tuple(bases)

        # 添加一个默认的排序
        if 'Meta' in attrs:
            if not hasattr(attrs['Meta'], 'ordering'):
                attrs['Meta'].ordering = ('-update_time',)

        # 时间字段在其他字段后面添加
        attrs.setdefault('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间'))
        attrs.setdefault('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间'))
        new_class = super().__new__(mcs, name, bases, attrs)
        return new_class
