# coding:utf-8
import re
from abc import ABC

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from user.models import UserInfo
from user.utils import get_user_by_account


class UserSerializer(Serializer):
    user_head = serializers.CharField()
    name = serializers.CharField()
    con_phone = serializers.CharField()
    gender = serializers.BooleanField()
    object = serializers.CharField()
    cls = serializers.CharField()
    qq = serializers.CharField()

    def validate_name(self, value):
        if 2 <= len(value) <= 8:
            return value
        else:
            return serializers.ValidationError("姓名长度应该在 2-8 个字符")

    def validate_con_phone(self, value):
        if re.match(r'^((13[0-9])|(17[0-1,6-8])|(15[^4,\\D])|(18[0-9]))\d{8}$', value):
            return value
        else:
            raise serializers.ValidationError("请输入正确的手机号")

    def validate_qq(self, value):

        if 6 <= len(value) <= 10:
            return value
        else:
            raise serializers.ValidationError("请输入正确的QQ号码")

    def validate_object(self, value):
        if not value:
            raise serializers.ValidationError("请输入正确的专业")
        else:
            return value

    def validate_cls(self, value):
        if not value:
            raise serializers.ValidationError("请输入正确的班级")
        else:
            return value

    def validate_gender(self, value):
        if value:
            return True
        else:
            return False

    def update(self, instance, validated_data):
        instance.cls = validated_data.get('cls', instance.cls)
        instance.con_phone = validated_data.get('con_phone', instance.con_phone)
        instance.object = validated_data.get('object', instance.object)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.name = validated_data.get('name', instance.name)
        instance.user_head = validated_data.get('user_head', instance.user_head)
        instance.qq = validated_data.get('qq', instance.qq)
        instance.save()
        return instance
class UserModelSerializer(ModelSerializer):
    token = serializers.CharField(max_length=1024, read_only=True, help_text="用户token")
    code = serializers.CharField(write_only=True, help_text="手机验证码")

    class Meta:
        model = UserInfo
        fields = (
            "con_phone", "user_head", "password", "id", "username", "token", "code", "cls", "object", 'qq', 'gender',
            'name')

        extra_kwargs = {
            "password": {
                "write_only": True,
            },
            "id": {
                "read_only": True,
            },
            'con_phone': {
            },
            'name': {
            },
            'cls': {
            },
            'object': {
            },
            'qq': {
            },
            'gender': {
            }

        }

    # 全局钩子  完成用户数据的校验
    def validate(self, attrs):

        phone = attrs.get("phone")
        password = attrs.get("password")
        sms_code = attrs.get("code")
        username = attrs.get("username")

        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', phone):
            raise serializers.ValidationError("手机号格式错误")

        if not re.match(r'^[0-pa-zA-Z]{3,16}$', username):
            raise serializers.ValidationError("用户名格式错误")
        if not re.match(r'^[0-pa-zA-Z.+*@#]{3,16}$', password):
            raise serializers.ValidationError("密码格式错误")
        # 验证手机号是否被注册
        try:
            user_phone = get_user_by_account(phone)
        except UserInfo.DoesNotExist:
            user_phone = None
        try:
            user_name = get_user_by_account(username)

        except UserInfo.DoesNotExist:
            user_name = None

        if user_phone:
            raise serializers.ValidationError("当前手机号已经被注册")
        if user_name:
            raise serializers.ValidationError("当前用户名已经被使用")

        redis_connection = get_redis_connection("sms_code")
        mobile_code = redis_connection.get("mobile_%s" % phone)
        if not mobile_code:
            raise serializers.ValidationError("验证码失效,请重新获取")
        if mobile_code.decode() != sms_code:
            redis_connection.incr('mobile_%s_time' % phone, 1)
            times = redis_connection.get('mobile_%s_time' % phone).decode()
            if times == 3:
                redis_connection.delete('mobile_%s_time')
                redis_connection.delete('mobile_%s')
                raise serializers.ValidationError("错误次数过多,请重新获取验证码")
            # 代表验证码有误
            # 为了防止暴力破解  可以设置一个手机号只能验证n次  累加
            raise serializers.ValidationError("验证码不一致")

        # 验证通过后将redis的验证码的删除
        redis_connection.delete("mobile_%s" % phone)
        return attrs

    def create(self, validated_data):
        """用户默认信息设置"""
        # 获取密码  对密码进行加密
        phone = validated_data.get('phone')
        password = validated_data.get("password")
        hash_password = make_password(password)

        # 处理用户名的默认值  随机字符串  手机号
        username = validated_data.get("username")
        # 保存数据
        user = UserInfo.objects.create(
            phone=phone,
            username=username,
            password=hash_password
        )

        # 为注册的用户手动生成token
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user
