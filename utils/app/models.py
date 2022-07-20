from django.db.models.base import ModelBase
from django.db import models
from django.contrib.auth import get_user_model  # UserModel的快捷方式，当然你也可以自己手动导入用户的Model

UserModel = get_user_model()


# 自定义 models.SET
def SET(value):
    if callable(value):
        def set_on_delete(collector, field, sub_objs, using):
            collector.add_field_update(field, value(sub_objs), sub_objs)  # 仅在回调函数中传递 sub_objs 参数
    else:
        def set_on_delete(collector, field, sub_objs, using):
            collector.add_field_update(field, value, sub_objs)
    set_on_delete.deconstruct = lambda: ("django.db.models.SET", (value,), {})
    return set_on_delete


# on_delete=models.SET() 的回调函数
def get_sentinel_user(sub_objs):
    # 获取准备更新的数据的owner键
    handover_id = 0  # 交接人ID
    for model in sub_objs:
        handover_id = model.owner.handover_id if hasattr(model, 'owner') else 0
        break
    if handover_id:  # 如果有交接人
        return handover_id
    else:
        return get_user_model().objects.get_or_create(username='admin')[0]


# 通用模型继承类
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
            if field.name != 'id' and not field.many_to_many and not field.one_to_many and not isinstance(field, (
            models.DateTimeField, models.DateField, models.TimeField)):
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


class OwnerModelClass(GenericModelClass):
    """元类"""
    def __new__(mcs, name, bases, attrs):
        # 如果 UserModel.handover_id 有值，则被关联用户准备删除时，将数据转移到 handover_id 的用户上
        attrs.setdefault('owner', models.ForeignKey(UserModel, on_delete=SET(get_sentinel_user), verbose_name='关联用户', help_text="关联用户自动填充", db_constraint=False))

        new_class = super().__new__(mcs, name, bases, attrs)
        return new_class
