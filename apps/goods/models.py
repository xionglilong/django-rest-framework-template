from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class GoodCategoryModel(models.Model):
    """
    商品类别
    """
    CATEGORY_TYPE = ((1, "一级类目"), (2, "二级类目"), (3, "三级类目"), )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父目录", help_text="父目录", related_name="sub_category", on_delete=models.CASCADE)
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    create_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodModel(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodCategoryModel, verbose_name="商品类目", on_delete=models.CASCADE)
    good_sn = models.CharField(max_length=50, default="", verbose_name="商品唯一货号", unique=True)
    name = models.CharField(max_length=100, verbose_name="商品名")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="商品销售量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    good_num = models.IntegerField(default=0, verbose_name="库存数")
    market_price = models.FloatField(default=0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格")
    brief_desc = models.TextField(max_length=500, verbose_name="商品简短描述")
    desc = models.TextField(verbose_name="内容", default='')
    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费")
    front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图", max_length=200)
    images = models.TextField('商品图片列表')
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")
    create_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ShoppingCartModel(models.Model):
    """
    购物车
    """
    owner = models.ForeignKey(UserModel, verbose_name="用户", on_delete=models.CASCADE)
    good = models.ForeignKey(GoodModel, verbose_name="商品", on_delete=models.CASCADE)
    num = models.IntegerField(default=0, verbose_name="购买数量")

    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ("owner", "good")

    def __str__(self):
        return "%s(%d)".format(self.good.name, self.num)


class OrderInfoModel(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待支付"),
    )

    owner = models.ForeignKey(UserModel, verbose_name="用户", on_delete=models.CASCADE)
    order_sn = models.CharField(max_length=60, null=True, blank=True, unique=True, verbose_name="订单号")  # 平台内的id
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="交易号")  # 支付宝那边的id
    pay_status = models.CharField(choices=ORDER_STATUS, default="paying", max_length=30, verbose_name="订单状态")
    message = models.CharField(max_length=200, verbose_name="订单留言")
    price_count = models.FloatField(default=0.0, verbose_name="订单金额")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")

    # 收货信息
    receive_address = models.CharField(max_length=100, default="", verbose_name="收货地址")
    receive_name = models.CharField(max_length=20, default="", verbose_name="签收人")
    receive_mobile = models.CharField(max_length=11, verbose_name="联系电话")

    create_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoodModel(models.Model):
    """
    订单的商品详情
    """
    order = models.ForeignKey(OrderInfoModel, verbose_name="订单信息", related_name="goods", on_delete=models.CASCADE)
    good = models.ForeignKey(GoodModel, verbose_name="商品", on_delete=models.CASCADE)
    num = models.IntegerField(default=0, verbose_name="商品数量")

    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
