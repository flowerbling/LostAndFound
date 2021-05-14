from django.db import models
from user.models import UserInfo


# Create your models here.
class GoodsInfo(models.Model):
    is_lost = models.BooleanField(default=True, verbose_name="是否为失物")
    name = models.CharField(max_length=16, verbose_name="物品名称")
    the_type_choices = (
        (0, '文件'),
        (1, '文具'),
        (2, '日常用品'),
        (3, '玩具'),
        (4, '电子产品'),
        (5, '衣服'),
        (6, '其他')
    )
    the_type = models.SmallIntegerField(choices=the_type_choices, verbose_name='物品类型', default=0)
    description = models.CharField(max_length=255, verbose_name='物品描述')
    date = models.DateTimeField(verbose_name="时间(拾取/丢失)")
    area = models.CharField(max_length=128, verbose_name='地点(拾取/丢失)')
    user = models.ForeignKey(to='user.UserInfo', on_delete=models.CASCADE, verbose_name='用户编号')
    status = models.BooleanField(default=True, verbose_name="是否有效")

    class Meta:
        db_table = 'laf_goods'
        verbose_name_plural = verbose_name = "物品信息"


class GoodsImage(models.Model):
    image_url = models.CharField(max_length=255, verbose_name="图片地址", blank=True, null=True)
    goods = models.ForeignKey(to="GoodsInfo", on_delete=models.CASCADE, verbose_name="物品编号")

    class Meta:
        db_table = "laf_goodsImage"
        verbose_name_plural = verbose_name = "物品图片"


class GoodsMessage(models.Model):
    content = models.CharField(max_length=255, verbose_name='留言内容')
    date = models.DateTimeField(auto_now=True, verbose_name='留言时间')
    goods = models.ForeignKey(to="GoodsInfo", on_delete=models.CASCADE, verbose_name='商品编号')
    user = models.ForeignKey(to="user.UserInfo", on_delete=models.CASCADE, verbose_name='用户编号')

    class Meta:
        db_table = "laf_goods_message"
        verbose_name_plural = verbose_name = "物品留言"
