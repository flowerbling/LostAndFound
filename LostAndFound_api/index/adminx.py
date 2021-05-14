# coding:utf-8

import xadmin

from index.models import *


class NavAdmin:
    list_display = ['name', "nav_url", 'orders']


xadmin.site.register(Nav, NavAdmin)
