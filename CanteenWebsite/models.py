from django.db import models


class Setting(models.Model):
    class Meta:
        verbose_name_plural = "设置"

    name = models.CharField(
        verbose_name="设置项",
        max_length=100,
        unique=True
    )
    value = models.TextField(
        verbose_name="值",
        blank=True
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = "商品分类"

    category_name = models.CharField(
        verbose_name="分类名称",
        max_length=50
    )

    def __str__(self):
        return self.category_name


class Goods(models.Model):
    URL_LENGTH = 500

    class Meta:
        verbose_name_plural = "商品"

    # 商品所在平台选项
    PLATFORM_TYPE_CHOICES = (
        ("淘宝", "淘宝"),
        ("天猫", "天猫"),
        ("其他", "其他"),
    )

    category = models.ForeignKey(
        verbose_name="商品一级类目",
        to=Category,
        on_delete=models.CASCADE
    )
    id = models.BigIntegerField(
        verbose_name="商品ID",
        primary_key=True
    )
    name = models.CharField(
        verbose_name="商品名称",
        max_length=100
    )
    picture = models.URLField(
        verbose_name="商品主图",
        max_length=URL_LENGTH,
        blank=True
    )
    url_affiliate = models.URLField(
        verbose_name="淘宝客链接",
        max_length=URL_LENGTH,
    )
    price = models.FloatField(
        verbose_name="商品价格",
        default=0
    )
    price_real = models.FloatField(
        verbose_name="商品实际购买价格",
        default=0,
        editable=False
    )
    commission_rate = models.FloatField(
        verbose_name="收入比率(%)",
        default=0
    )
    commission = models.FloatField(
        verbose_name="佣金",
        default=0
    )
    shop_name = models.CharField(
        verbose_name="店铺名称",
        max_length=50,
        blank=True
    )
    platform_type = models.CharField(
        verbose_name="平台类型",
        choices=PLATFORM_TYPE_CHOICES,
        max_length=10,
        default="其他"
    )
    coupon_money = models.CharField(
        verbose_name="优惠券面额",
        max_length=50,
        blank=True
    )
    url_coupon = models.URLField(
        verbose_name="优惠券链接",
        max_length=URL_LENGTH,
        blank=True
    )
    coupon_time_start = models.DateField(
        verbose_name="优惠券开始时间",
        auto_now=True
    )
    coupon_time_end = models.DateField(
        verbose_name="优惠券结束时间",
        blank=True
    )
    url_affiliate_coupon = models.URLField(
        verbose_name="商品优惠券推广链接",
        max_length=URL_LENGTH,
        blank=True
    )

    def __str__(self):
        return self.name
