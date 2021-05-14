# coding:utf-8
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from goods.models import GoodsInfo, GoodsImage, GoodsMessage
from user.models import UserInfo
from user.serializers import UserSerializer


class GoodsImageModelSerializer(ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ["goods", 'image_url']


class GoodsMessageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsMessage
        fields = ['user', 'goods', 'content', 'date']

    # def get_message_user(self, obj):
    #     query = obj.user
    #     data = {'con_phone': query.con_phone, 'name': query.name, 'user_head': str(query.user_head),
    #             'gender': query.gender, 'qq': query.qq, 'cls': query.cls, 'object': query.object}
    #     return data


class GoodsModelSerializer(ModelSerializer):
    images = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    goods_message = serializers.SerializerMethodField()

    # user = UserSerializer()

    class Meta:
        model = GoodsInfo
        fields = ['id', 'name', 'the_type', 'is_lost', 'area', 'date', 'description', 'images', 'user', 'goods_message',
                  'status']

    def get_images(self, obj):
        query_set = obj.goodsimage_set.all()
        data = [{'image_url': str(query.image_url)} for query in query_set]
        return data

    def get_user(self, obj):
        query = obj.user
        data = {'con_phone': query.con_phone, 'name': query.name, 'user_head': str(query.user_head),
                'gender': query.gender, 'qq': query.qq, 'cls': query.cls, 'object': query.object}
        return data

    def get_goods_message(self, obj):
        query_set = obj.goodsmessage_set.all()
        data = [
            {'date': query.date, 'content': query.content, 'name': query.user.name, 'con_phone': query.user.con_phone,
             'qq': query.user.qq}
            for query in query_set]
        return data


    def validate(self, attrs):
        name = attrs.get('name')
        the_type = attrs.get('the_type')
        is_lost = attrs.get('is_lost')
        area = attrs.get('area')
        date = attrs.get('date')
        description = attrs.get('description')
        user = UserInfo.objects.get(id=self.initial_data['user'])
        attrs['user'] = user
        if is_lost:
            attrs['is_lost'] = True
        else:
            attrs["is_lost"] = False
        if not name:
            raise serializers.ValidationError("请输入名字")
        if not 0 <= the_type <= 6:
            raise serializers.ValidationError("请选择正确的类型")
        if not area or not date:
            raise serializers.ValidationError("时间和地点不完整")
        if not description:
            raise serializers.ValidationError("请输入描述")
        return attrs
