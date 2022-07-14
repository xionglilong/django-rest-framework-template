# 导入人员信息测试数据（独立使用django的model的方式）
import sys
import os
import django

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(pwd, '../../../'))  # 重要：将项目根目录加入包搜索路径
sys.path.append(os.path.join(pwd, '../../../apps/'))  # 重要：将项目根目录的apps加入搜集路径
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
django.setup()

# 初始化环境后，才能导入模块

from users.models import SmsCodeModel

code_data = [
    {'mobile': '15800000000', 'code': '1234'}
]


def create_sms_code():
    for code_dict in code_data:
        code_instance = SmsCodeModel()
        code_instance.mobile = code_dict['mobile']
        code_instance.code = code_dict['code']
        code_instance.save()


if __name__ == '__main__':
    create_sms_code()
