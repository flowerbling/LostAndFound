# coding:utf-8

import xadmin

from user.models import *


class UserInfoAdmin:
    list_display = ['username', 'phone', 'email', 'user_head']



