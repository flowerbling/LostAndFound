from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserInfo(AbstractUser):
    phone = models.CharField(max_length=11, verbose_name='手机号', unique=True,null=True)
    con_phone = models.CharField(max_length=11,verbose_name='联系电话',null=True)
    user_head = models.ImageField(upload_to='user_head', verbose_name="用户头像", blank=True, null=True,
                                  default='user_head/default_head_pic.png')
    name = models.CharField(max_length=16, verbose_name="真实姓名", null=True)
    object = models.CharField(max_length=32, verbose_name='所在专业', null=True)
    cls = models.CharField(max_length=32, verbose_name='所在班级', null=True)
    qq = models.CharField(max_length=11, verbose_name='QQ号码', null=True)
    gender = models.BooleanField(default=True, verbose_name='性别')

    class Meta:
        db_table = 'laf_user'
        verbose_name_plural = verbose_name = "用户信息"

# Create your models here.
