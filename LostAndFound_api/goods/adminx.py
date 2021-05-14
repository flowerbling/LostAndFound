# coding:utf-8
import xadmin

from goods.models import GoodsInfo, GoodsImage, GoodsMessage


class GoodsInfoAdmin:
    list_display = ['name', 'description', 'date', 'area']


#
class GoodsImageAdmin:
    list_display = ['id', 'goods', 'image_url']


class GoodsMessageAdmin:
    list_display = ['id', 'goods', 'user', 'content']


xadmin.site.register(GoodsInfo, GoodsInfoAdmin)
xadmin.site.register(GoodsImage, GoodsImageAdmin)
xadmin.site.register(GoodsMessage, GoodsMessageAdmin)
