from rest_framework import serializers
from .models import GoodModel, GoodCategoryModel, OrderInfoModel, OrderGoodModel
from utils.alipay_api import AlipayAPI


# 商品类别 数据序列化器
class CategorySerializer(serializers.ModelSerializer):
    # sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodCategoryModel
        fields = "__all__"


# 商品 数据序列化器
class GoodSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = serializers.ListField()

    class Meta:
        model = GoodModel
        fields = "__all__"


# 订单的商品 数据序列化器
class OrderGoodSerializer(serializers.ModelSerializer):
    good = GoodSerializer(many=False)

    class Meta:
        model = OrderGoodModel
        fields = "__all__"


# 订单详情 数据序列化器
class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, order_sn, price_count, good_name):
        pay_url = AlipayAPI().page_pay(order_sn, price_count, good_name)
        return pay_url

    class Meta:
        model = OrderInfoModel
        fields = "__all__"
