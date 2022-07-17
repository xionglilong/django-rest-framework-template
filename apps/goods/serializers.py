from rest_framework import serializers
from .models import GoodModel, GoodCategoryModel, OrderInfoModel, OrderGoodModel
from utils.alipay_api import AlipayAPI


# 自定义递归字段
class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


# 商品类别 数据序列化器
class GoodCategorySerializer(serializers.ModelSerializer):
    # children = RecursiveSerializer(many=True)  # 方法一
    children = serializers.SerializerMethodField()  # 方法二：注意需要跟下面的get_children()一起。(这里名字和外键反向关联名字是一致的)

    # 简单的树状需求，可以就这么写
    def get_children(self, obj):
        if obj.children:
            return GoodCategorySerializer(obj.children, many=True).data
        return None

    class Meta:
        model = GoodCategoryModel
        fields = "__all__"


# 商品 数据序列化器
class GoodSerializer(serializers.ModelSerializer):
    category = GoodCategorySerializer()
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
