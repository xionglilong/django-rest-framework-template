# api接口：https://opendocs.alipay.com/open/028r8t?scene=22
# sdk文档：https://opendocs.alipay.com/open/02no41
# 网站支付：https://opendocs.alipay.com/open/270/

import logging
import traceback
from urllib.parse import urlparse, parse_qs, quote_plus
from base64 import decodebytes, encodebytes
import json
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.response import AlipayTradePagePayResponse
from alipay.aop.api.util.SignatureUtils import verify_with_rsa  # 验签

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a', )
logger = logging.getLogger('')


class AlipayAPI:
    __instance = None  # 类变量，是否被实例化过
    __is_init = False  # 类变量，是否执行过 __init__

    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:  # 如果是第一次实例化
            cls.__instance = super().__new__(cls, *args, **kwargs)  # 将类的实例和一个类变量 _instance 关联起来
        return cls.__instance

    def __init__(self):
        if not AlipayAPI.__is_init:
            AlipayAPI.__is_init = True
        # 实例化客户端
        self.alipay_client_config = AlipayClientConfig()
        self.alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'  # 沙箱环境
        # self.alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'  # 正式环境
        self.alipay_client_config.app_id = '2021000121625722'
        self.alipay_client_config.app_private_key = 'MIIEpAIBAAKCAQEAx/awkKOP9qTiEWrpjNoZ9SAfBI791Pv31o3wAZSnfmSP8N9aWE4gXVPqFPMri/dDE+vOwhm6cCL6DuLgIy2MCdyY21+TrZTIJABXstAcfqSw9PM6I4H2CWVGKO5oJ/Z09QfGkJ8vK4nrmQo3f6G8oMFIQEHDXqyEyvXH5zYb47oA0dsEXZJsVPqUdEa46yiOM0ekjbHE58koOp/5qfbU5o5gRuNK+GWpeykVrxO3X61+A9P4gFE4tf1oZm15M1dUvdEqNkis5aikJzd+SPZqaq9Qg9yLxPiXjysJ8ZfUTUeabZPUyVhkUAg4ULxhRnDPDfRhAqy9zm58nVf6MArCpQIDAQABAoIBAQCr6hLyxyxGSItzng8c4YXfkLYaHTVtnxL8ixsEwOEfcSWvWNc7hC+fDT36tPWDaBlrTxh7F9OKBQgnNDavB8GV2Oox8IHugjNvgDvlp7ZXyw+4CES7skfs2/ztw8oYUXNMFltIixLqw7Ch6n68ZDjfnEyZsfBdvMSOGbC7v3FK3mIthnHIEkmHqhINDfzk4fw5JYmNChYJi50SCJHiLVYCMeph0xNaFXEi91sp0QWQYP+2i1gZ8//xjhJxCJycrU+Z/JIuuTH0MRCfmo7PSH2PY6rXtOEsHf/Y31hw4w1ObOwyhD1/FSSFx/1j8zuMfDwTGGbumgQaiiYSpBW+xvYBAoGBAOYmCDDCU9c5bHHZ09c3zbUrbmxpZdC9s/04bcwhieFId3YgpkPf944NdVbcXM1CfmzsOAJ6otrJVwUU065yZ4tUgD5hi+fQiBqH4zBP7W8ZPBjzNN/xLaU+U/ZRF4MZEzy/DV/dmHiM0pBHFUkSwX6NbW01J4AnDznhagDxRYcVAoGBAN5srxl5bBVDKIjILK88gGPwZV2RlDx7DxFbg53DdWIw08uQRwlKCq4qBQdCd07dXPANyAVo5Jb3PHzW1tTMTg3uS4XSuQ8sA0FlRFGQGeXfkNSle9TS0KvqH7sLo8PNjBk0Uh2GXNsaD6h+CWHYMpCo2m9Rfwyiw4rdCG7tcDFRAoGBALKBRxMCdmLVQB5h9CPWPW/KWuAtM3Ie4Q6DCO4uCTI5saZmlm7ItMpx99PCIRx2+XXkFWEe21dUmHDxgWmphFQV204G/Kt1G0twoC6ln6Pu76TuZdFXz6591EOVC+Z7uWcBTA9R4WOG3f5Xk9PUf013xirQ8m08XlvnUP+gIuwtAoGAYUPf0mEBvc6PhDkdKUho0MtIWIGX9FbQAQQm6y+VPmohxCwElHBXeVAQwNr093zf7m3oYU08YTQetGzypz3siDUDu7KpkJPrnIZfONeuK5L3b7YqD6hc7kDEvXPamn5hXIg/vH+MTZf47vKmwa3cdtwQIYve5jSrFCeST4fvfvECgYAdK27772foR1C7CrBzRO+MpqvWeDfQyAQ5cyM6Qx4ri4nGCmF70Nrw9KbEfw9r2IlivkeSzvTuaqtSev4ZZaIVmJIFgWX5k+6y5a7B9alV3jElzsKrPNi+f+5aIeU+iJC1mm+bKD5j/7WaI/JP9REhAYTbL/gjyRYKb/Q8TUuzKw=='
        self.alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAx/awkKOP9qTiEWrpjNoZ9SAfBI791Pv31o3wAZSnfmSP8N9aWE4gXVPqFPMri/dDE+vOwhm6cCL6DuLgIy2MCdyY21+TrZTIJABXstAcfqSw9PM6I4H2CWVGKO5oJ/Z09QfGkJ8vK4nrmQo3f6G8oMFIQEHDXqyEyvXH5zYb47oA0dsEXZJsVPqUdEa46yiOM0ekjbHE58koOp/5qfbU5o5gRuNK+GWpeykVrxO3X61+A9P4gFE4tf1oZm15M1dUvdEqNkis5aikJzd+SPZqaq9Qg9yLxPiXjysJ8ZfUTUeabZPUyVhkUAg4ULxhRnDPDfRhAqy9zm58nVf6MArCpQIDAQAB'
        self.client = DefaultAlipayClient(self.alipay_client_config, logger)

    # 网站付款链接
    def page_pay(self, order_id='', price='', good_name='', **kwargs):
        # 构造请求参数对象
        model = AlipayTradePagePayModel()
        model.out_trade_no = order_id  # 平台订单号，数据库中必须唯一
        model.total_amount = price  # 价格
        model.subject = good_name  # 商品名称
        model.product_code = "FAST_INSTANT_TRADE_PAY"
        model.from_alipay_dict(kwargs)  # 更多参数

        request = AlipayTradePagePayRequest(biz_model=model)
        # request.notify_url = 'http://api.example.com/alipay/return/'  # 订单付款成功的回调地址（用户在支付宝app的订单页付款成功也会调用）（异步回调）
        request.return_url = 'http://www.example.com/alipay/return/'  # 网页付款成功后跳转的地址（用户扫码后关闭页面在手机支付成功是没有跳转的）
        # 执行API调用
        pay_url = self.client.page_execute(request, http_method='GET')
        return pay_url

    # 验签
    def verify_from_return_url(self, return_url):

        # 取出带签名的数据
        parse_object = urlparse(return_url)
        param_dict = parse_qs(parse_object.query)  # url参数的字典
        # 整理数据格式
        param_dict = {key: value[0] for key, value in param_dict.items()}
        return self.verify_from_dict(param_dict)

    # 验签
    def verify_from_dict(self, param_dict: dict) -> bool:
        # 支付宝公钥（开放平台查询）
        alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy8NIxcBtphAltjftiHfMAYRgIgSt6LDfSGrRIOVmkOiwbocpo5eX3F5WYlpEzlFghuMZ4DpbyRb9M8Gwjz5R4BgzlPR/qwAKcdhCqJDfS0L0HE9cqJWFoclgqokH44LN/Z1Hyc9JUN2x71LhU/80tK2v9R+hawjHYPPhgadS94xq8AfLHGELklgkbSWxJPi3blhS1cgoSCHoKdO0ywPni0j6IleDEFoeoHG1jWrkEuUsVd/eB6O07aWppndCN5uzQp/fdJUSb1uV1T88EKA42S92r6BZ98Rt+Zgx+CU4sb7jb+EtyVsGVLnzuFADRBA/Wpw4YVk8lp7VKdfRJr0gYQIDAQAB'

        # 删除不属于签名的内容
        ali_sign = param_dict.pop('sign')  # 阿里的签名。需要弹出来，因为不属于签名内容。
        if 'sign_type' in param_dict:
            sign_type = param_dict.pop('sign_type')  # 这里只是删除掉，不属于签名的内容。这步骤很重要，否则会验签失败。

        # 排序
        query_clean_list = self.__ordered_data(param_dict)

        # 生成message
        message_str = "&".join("{0}={1}".format(k, v) for k, v in query_clean_list)

        # 验签
        message_bytes = message_str.encode()  # 转为utf-8字节码
        return verify_with_rsa(alipay_public_key, message_bytes, ali_sign)

    @staticmethod
    def __ordered_data(data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类似的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])


if __name__ == '__main__':
    # 调试网页支付
    # pay_url = AlipayAPI().page_pay(order_id='20150320010101003', price="88.88", good_name='Iphone6 16G')
    # print(pay_url)

    # 验签
    response_url = "http://www.example.com/?charset=utf-8&out_trade_no=20150320010101003&method=alipay.trade.page.pay.return&total_amount=88.88&sign=NLYr2LPsMQy4LOCXytG5%2FA2XGdzMhHqK5vUVEWDhv683RgDxds5zQQjQkyfanFvbEh8L49o%2BUj7jTZrlX4rKHAQE1Bx7aOP9dmGxfEy%2BTM%2FWWA%2Bc8%2BuwDLun5QqobDcg9C9I9Hi066DHNuJnz4sVyC4dbydJwcdRhYs9ewHcRIMaMymGat3oSf84CJq9rtqtxh16L%2FmD7VtCP5eDngG7zGG5Ji48T5c%2FGygavuieJ1dj1TM1uRXzO%2BvMB3cE72GRSgf%2FxQEbJcwtfJ9szheCkS3liIxha6%2B5SukBpoOqU6F8YTb3cU%2FQLj6LI1%2FPQZ8RsZgBSVuGcquVg1Bi%2FYU5fQ%3D%3D&trade_no=2022071622001423620502188224&auth_app_id=2021000121625722&version=1.0&app_id=2021000121625722&sign_type=RSA2&seller_id=2088621987694550&timestamp=2022-07-16+17%3A53%3A02"
    result = AlipayAPI().verify_from_return_url(response_url)
    print(result)
