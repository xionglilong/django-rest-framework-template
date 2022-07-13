from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


# 使用阿里云接口发送短信
def aliyun_send_sms(mobile, code):
    # 使用AK&SK初始化账号Client
    config = open_api_models.Config(access_key_id='XXXX', access_key_secret='XXXX')
    config.endpoint = f'dysmsapi.aliyuncs.com'
    client = Dysmsapi20170525Client(config)

    send_sms_request = dysmsapi_20170525_models.SendSmsRequest(sign_name='阿里云短信测试', template_code='SMS_154950909',
                                                               phone_numbers=mobile,
                                                               template_param='{"code":"%s"}' % code)
    runtime = util_models.RuntimeOptions()
    try:
        # 复制代码运行请自行打印 API 的返回值
        result = client.send_sms_with_options(send_sms_request, runtime)
        print(result)
    except Exception as error:
        # 如有需要，请打印 error
        UtilClient.assert_as_string(error.message)
        print(error)


if __name__ == '__main__':
    # Sample.main(sys.argv[1:])
    aliyun_send_sms('15800000000', '1234')
