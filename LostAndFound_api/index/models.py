from django.db import models


# Create your models here.
class Nav(models.Model):
    """
    导航栏表
    """
    name = models.CharField(max_length=32, verbose_name='导航栏名')
    nav_url = models.CharField(max_length=128, verbose_name='导航栏链接')
    type = models.BooleanField(default=0, verbose_name='导航类型')
    orders = models.IntegerField(default=1, verbose_name='排序')

    class Meta:
        db_table = 'laf_nav'
        verbose_name_plural = verbose_name = "导航栏"
