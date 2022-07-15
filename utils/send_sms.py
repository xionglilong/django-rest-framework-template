# 使用aliyun接口发送验证码
# https://help.aliyun.com/document_detail/419273.html
# https://help.aliyun.com/document_detail/215764.html

import random
import re
from datetime import datetime, timedelta
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from users.models import SmsCodeModel


class AliyunSendSMS:
    __instance = None  # 类变量，是否被实例化过
    __is_init = False  # 类变量，是否执行过 __init__

    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:  # 如果是第一次实例化
            cls.__instance = super().__new__(cls, *args, **kwargs)  # 将类的实例和一个类变量 _instance 关联起来
        return cls.__instance

    def __init__(self):
        if not AliyunSendSMS.__is_init:
            AliyunSendSMS.__is_init = True
            # 使用AK&SK初始化账号Client
            self.config = open_api_models.Config(access_key_id='XXXX', access_key_secret='XXXX')
            self.config.endpoint = f'dysmsapi.aliyuncs.com'
            self.client = Dysmsapi20170525Client(self.config)

    # 发送验证码
    def send_code(self, mobile: str) -> dict:
        # 手机号格式检查
        if not re.match(r"^1[358]\d{9}$|^147\d{8}$|^176\d{8}$", mobile):
            return {'success': False, 'message': '非法手机号', 'code': ''}
        # 发送频率限制
        before_time = datetime.now() - timedelta(hours=0, minutes=0, seconds=50)
        if SmsCodeModel.objects.filter(create_time__gt=before_time, mobile=mobile):
            return {'success': False, 'message': '发送频率过快', 'code': ''}

        code = str(random.randint(100000, 999999))
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(sign_name='XX', template_code='SMS_XXXXXXXX',
                                                                   phone_numbers=mobile,
                                                                   template_param='{"code":"%s"}' % code)
        runtime = util_models.RuntimeOptions()
        try:
            result = self.client.send_sms_with_options(send_sms_request, runtime)
            # 返回的结果
            success = result.body.code
            message = result.body.message

            if success == 'OK':
                success = True
                SmsCodeModel(code=code, mobile=mobile).save()  # 保存到数据库
            else:
                success = False

            return {'success': success, 'message': message}

        except Exception as error:
            print(error)
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    # 查询有效验证码
    @staticmethod
    def select_code(mobile) -> dict:
        code_queryset = SmsCodeModel.objects.filter(mobile=mobile).order_by('-create_time')  # get()方法如果没数据会报错还有额外处理，所以filter()更方便
        if code_queryset:
            last_code = code_queryset[0]  # 只取数据库最近的一条
            before_time = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)  # 有效期5分钟
            if before_time > last_code.create_time:
                return {'success': False, 'message': '验证码已过期', 'code': ''}
            return {'success': True, 'message': '', 'code': last_code.code, 'model_object': last_code}
        else:  # 数据库都没有记录发送过的验证码
            return {'success': False, 'message': '请先发送验证码', 'code': ''}

    # 核验验证码
    def validate_code(self, mobile, code) -> dict:
        result = self.select_code(mobile)
        if result['success']:  # 如果数据库有 有效验证码，则对比
            if result['code'] == str(code):
                result['model_object'].used = True
                result['model_object'].save()
                return {'success': True, 'message': '', 'code': ''}
            else:
                return {'success': False, 'message': '验证码错误', 'code': ''}
        else:  # 如果数据库没有 有效验证码，向上返回
            return result


if __name__ == '__main__':
    # Sample.main(sys.argv[1:])
    AliyunSendSMS().send_code('15838293829')
