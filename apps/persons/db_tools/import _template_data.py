# 导入人员信息测试数据（独立使用django的model的方式）
import sys
import os
import django

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(pwd, '../../../'))  # 重要：将项目根目录加入包搜索路径
sys.path.append(os.path.join(pwd, '../../../apps/'))  # 重要：将项目根目录的apps加入搜集路径
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
django.setup()

from django.contrib.auth import get_user_model  # UserModel的快捷方式，当然你也可以自己手动导入用户的Model
UserModel = get_user_model()
user1 = UserModel.objects.get(username="admin")

person_data = [
    {'name': '张三', 'sex': 1, 'age': 23, 'email': 'doicui@qq.com', 'icon': 'head/default.jpg', "owner": user1},
]

from persons.models import PersonModel  # 先初始化环境，这里才能导入模块

for person_dict in person_data:
    person_instance = PersonModel()
    person_instance.name = person_dict['name']
    person_instance.sex = person_dict['sex']
    person_instance.age = person_dict['age']
    person_instance.mail = person_dict['email']
    person_instance.icon = person_dict['icon']
    person_instance.owner = person_dict['owner']
    person_instance.save()

