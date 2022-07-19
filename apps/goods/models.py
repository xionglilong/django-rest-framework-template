from django.db import models
from django.contrib.auth import get_user_model
from utils.app.models import GenericModelClass, GenericModel, OwnerModelClass

UserModel = get_user_model()


class GoodCategoryModel(metaclass=GenericModelClass):
    """
    商品类别
        类别的外键是关联到自己，可以做无限循环的树状结构。但是一般用第三方包实现，比如：django-mptt、django-treebeard
    """
    CATEGORY_TYPE = ((1, "一级类目"), (2, "二级类目"), (3, "三级类目"), )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    description = models.TextField(default="", verbose_name="类别描述", help_text="类别描述", blank=True)
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别", default=1)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, db_constraint=False, related_name='children', verbose_name='父级类别')  # db_constraint=False代表不在数据库层面创建约束
    # db_constraint 控制是否在数据库中为此外键创建约束，默认为True。在数据库中创建外键约束是数据库规范中明令禁止的行为
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name


class GoodModel(metaclass=GenericModelClass):
    """
    商品
    """
    name = models.CharField(max_length=100, verbose_name="商品名")
    category = models.ForeignKey(GoodCategoryModel, verbose_name="商品类目", on_delete=models.CASCADE)
    good_sn = models.CharField(max_length=50, default="", verbose_name="商品唯一货号", unique=True)
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="商品销售量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    good_num = models.IntegerField(default=0, verbose_name="库存数")
    market_price = models.FloatField(default=0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格")
    brief_desc = models.CharField(max_length=500, verbose_name="商品简短描述")
    description = models.TextField(verbose_name="内容", default='')
    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费")
    front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图", max_length=200)
    images = models.CharField('商品图片列表', max_length=1024)
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class ShoppingCartModel(metaclass=OwnerModelClass):
    """
    购物车
    """
    good = models.ForeignKey(GoodModel, verbose_name="商品", on_delete=models.CASCADE)
    num = models.IntegerField(default=0, verbose_name="购买数量")

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ("owner", "good")
        # ordering = ('-create_time',)  # admin列表页默认初始排序规则

    def __str__(self):
        return "%s(%d)".format(self.good.name, self.num)


class OrderInfoModel(metaclass=OwnerModelClass):
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

    order_sn = models.CharField(max_length=60, null=True, blank=True, unique=True, verbose_name="订单号")  # 平台内的id
    owner = models.ForeignKey(UserModel, verbose_name="用户", on_delete=models.CASCADE)
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="交易号")  # 支付宝那边的id
    pay_status = models.CharField(choices=ORDER_STATUS, default="paying", max_length=30, verbose_name="订单状态")
    message = models.CharField(max_length=200, verbose_name="订单留言")
    price_count = models.FloatField(default=0.0, verbose_name="订单金额")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")

    # 收货信息
    receive_address = models.CharField(max_length=100, default="", verbose_name="收货地址")
    receive_name = models.CharField(max_length=20, default="", verbose_name="签收人")
    receive_mobile = models.CharField(max_length=11, verbose_name="联系电话")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name


class OrderGoodModel(GenericModel, metaclass=GenericModelClass):
    """
    订单的商品详情
    """
    order = models.ForeignKey(OrderInfoModel, verbose_name="订单信息", related_name="goods", on_delete=models.CASCADE)
    good = models.ForeignKey(GoodModel, verbose_name="商品", on_delete=models.CASCADE, db_constraint=False)
    num = models.IntegerField(default=0, verbose_name="商品数量")

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
