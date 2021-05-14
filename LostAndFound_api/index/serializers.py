# coding:utf-8


from rest_framework.serializers import ModelSerializer

from index.models import *


class NavModelSerializer(ModelSerializer):
    class Meta:
        model = Nav
        fields = ['name', 'nav_url', 'orders']
