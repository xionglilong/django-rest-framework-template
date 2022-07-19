# 需要在apps.py中重载ready()方法，将该模块导入
# 文档：https://docs.djangoproject.com/zh-hans/4.0/ref/signals/

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import random

UserModel = get_user_model()


# UserModel增加数据时的操作
@receiver(post_save, sender=UserModel)  # 接收UserModel传递过来的post_save信号
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:  # 如果传递过来的是创建操作，而不是更新操作
        # 密码为密文
        password = instance.password
        instance.set_password(password)
        # 给一个初始昵称
        instance.name = '用户' + str(random.randint(100000, 999999))
        instance.save()
