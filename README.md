## 项目介绍
本项目是一个django-rest-framework的模板项目，可以直接克隆后基于本项目做二次开发。

项目使用 python3.10、django4.0、django-rest-framework3.13 进行开发。

## 项目提供的功能：

**项目优化:**
- 目录组织优化
- 配置文件优化
- API文档生成优化
- 跨域优化
- 虚拟环境优化
- admin管理后台功能优化
- 模型功能优化

**第三方API接口:**
- 阿里云短信验证码接口
- 阿里云oss接口
- 支付宝付款接口

**示例app:**
- app：自定义用户和部门
- app: 人员信息管理
- app: 文章管理
- app: 商品管理





## 项目安装
```shell
mkdir .venv
pipenv install
```

## 依赖安装
```shell
# 在Linux系统中，oss2包需要python-devel依赖，不然会导致上传下载效率非常低
apt-get install python-dev
```