# https://help.aliyun.com/document_detail/52834.html
# 上传文件到OSS

import oss2
from itertools import islice


class AliyunOSS:
    __instance = None  # 类变量，是否被实例化过
    __is_init = False  # 类变量，是否执行过 __init__

    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:  # 如果是第一次实例化
            cls.__instance = super().__new__(cls, *args, **kwargs)  # 将类的实例和一个类变量 _instance 关联起来
        return cls.__instance

    def __init__(self):
        if not AliyunOSS.__is_init:
            AliyunOSS.__is_init = True

            # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
            self.auth = oss2.Auth('XXXX', 'XXXX')
            # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
            self.endpoint = 'https://oss-cn-hangzhou.aliyuncs.com'
            # 填写Bucket名称。
            self.bucket = oss2.Bucket(self.auth, self.endpoint, 'world-seo-django-media', connect_timeout=30)

    # 上传文件到OSS
    def update(self, oss_relative_url, data, mode='stream', local_file_path=''):
        # 在OSS中，操作的基本数据单元是文件（Object）
        # 上传文件（Object）时，如果存储空间（Bucket）中已存在同名文件且用户对该文件有访问权限，则新添加的文件将覆盖原有文件。
        if mode == 'stream':  # 上传网络流
            # self.bucket.put_object('<oss_file_relative_path>', '<network_stream>')
            self.bucket.put_object(oss_relative_url, data)
        if mode == 'local_file':  # 上传本地文件
            # self.bucket.put_object_from_file('demo/demo.txt', 'D:\\demo\\demo.txt')
            self.bucket.put_object_from_file(oss_relative_url, local_file_path)

    # 下载OSS文件到本地
    def download(self):
        # <yourObjectName>由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
        # <yourLocalFile>由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
        self.bucket.get_object_to_file('<yourObjectName>', '<yourLocalFile>')

    # 查看文件列表
    def list(self):
        file_list = []
        for b in islice(oss2.ObjectIterator(self.bucket), 10):
            file_list.append(b.key)
        return file_list

    # 删除文件
    def delete(self):
        # <yourObjectName>表示删除OSS文件时需要指定包含文件后缀，不包含Bucket名称在内的完整路径，例如abc/efg/123.jpg。
        self.bucket.delete_object('<yourObjectName>')


if __name__ == '__main__':
    result = AliyunOSS().list()
    print(result)


