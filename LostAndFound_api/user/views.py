import os
import random
import re
import uuid

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.filters import OrderingFilter

from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status

from goods.MyFilter import LimitFilter
from goods.models import GoodsInfo
from goods.pagination import MyPagination
from goods.serializers import GoodsModelSerializer
from libs.geetest import GeetestLib
from user import contastnt
from user.models import UserInfo
from user.serializers import UserModelSerializer, UserSerializer

# 获取验证码所需要的 id 和 key
from user.utils import get_user_by_account
from utils.send_msg import Message

pc_geetest_id = "1ea3ed8b35299a931b6a3883ec4a05be"
pc_geetest_key = "9a13879615c1ae2500e356417cd5bcf9"


# 验证码 视图类
class CaptchaAPIView(APIView):
    user_id = 0
    status = False

    # 前端发送请求验证账号 账号存在则返回验证码所需要的gt
    def get(self, request, *args, **kwargs):
        username = request.query_params.get("username")
        user = get_user_by_account(username)
        if user is None:
            return Response({"message": "用户不存在"}, status=http_status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)

        response_str = gt.get_response_str()
        return Response(response_str)

    # 验证码验证后  验证是否成功
    def post(self, request, *args, **kwargs):
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        if self.user_id:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)


class MobileLoginCheckAPIView(APIView):
    def get(self, request):
        phone = request.query_params.get("phone")
        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return Response({"message": "手机号格式不正确"},
                            status=http_status.HTTP_400_BAD_REQUEST)

        user = get_user_by_account(phone)

        if user is None:
            return Response({"message": "手机号还没有注册,先去注册一个账号吧"},
                            status=http_status.HTTP_400_BAD_REQUEST)

        return Response({"message": "OK"})


class MobileCheckAPIView(APIView):
    def get(self, request):
        phone = request.query_params.get("phone")
        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return Response({"message": "手机号格式不正确"},
                            status=http_status.HTTP_400_BAD_REQUEST)

        user = get_user_by_account(phone)

        if user is not None:
            return Response({"message": "手机号已经被注册"},
                            status=http_status.HTTP_400_BAD_REQUEST)

        return Response({"message": "OK"})


class UsernameCheckAPIView(APIView):
    def get(self, request):
        username = request.query_params.get("username")
        # 验证用户名格式
        if not re.match(r'^[0-pa-zA-Z]{3,16}$', username):
            return Response({"message": "用户名格式不正确"},
                            status=http_status.HTTP_400_BAD_REQUEST)

        user = get_user_by_account(username)

        if user is not None:
            return Response({"message": "用户名已经被使用"},
                            status=http_status.HTTP_400_BAD_REQUEST)

        return Response({"message": "OK"})


class SendMessageAPIView(APIView):
    """短信注册业务"""

    def get(self, request, *args, **kwargs):
        """
        获取验证码   为手机号生成验证码并发送
        :param request:
        :return:
        """
        phone = request.query_params.get("phone")

        # 获取redis连接
        redis_connection = get_redis_connection("sms_code")
        mobile_code = redis_connection.get("sms_%s" % phone)

        if mobile_code is not None:
            return Response({"message": "您已经在60s内发送过短信了，请稍等~"},
                            status=http_status.HTTP_400_BAD_REQUEST)

        code = "%06d" % random.randint(0, 999999)

        redis_connection.setex("sms_%s" % phone, contastnt.SMS_EXPIRE_TIME, code)  # 验证码间隔时间
        redis_connection.setex("mobile_%s" % phone, contastnt.CODE_EXPIRE_TIME, code)  # 验证码有效期
        redis_connection.set('mobile_%s_time' % phone, 0)
        try:
            message = Message(contastnt.API_KEY)
            message.send_message(phone, code)
        except:
            return Response({"message": "验证码发送失败"},
                            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "短信发送成功"},
                        status=http_status.HTTP_200_OK)


class PhoneLoginAPIView(APIView):
    def get(self, request, *args, **kwargs):
        phone = request.query_params.get('phone')
        code = request.query_params.get('code')
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return Response({"message": "手机号有误"}, status=http_status.HTTP_400_BAD_REQUEST)
        if not re.match(r'^\d{6}$', code):
            return Response({"message": "验证码有误"}, status=http_status.HTTP_400_BAD_REQUEST)
        try:
            user_phone = get_user_by_account(phone)
        except UserInfo.DoesNotExist:
            user_phone = None
        if not user_phone:
            return Response({"message": "手机号不存在"}, status=http_status.HTTP_400_BAD_REQUEST)
        redis_connection = get_redis_connection("sms_code")
        mobile_code = redis_connection.get("mobile_%s" % phone)
        if not mobile_code:
            return Response({"message": "验证码失效,请重新获取"}, status=http_status.HTTP_400_BAD_REQUEST)
        if mobile_code.decode() != code:
            # 代表验证码有误
            # 为了防止暴力破解  可以设置一个手机号只能验证n次  累加
            redis_connection.incr('mobile_%s_time' % phone, 1)
            times = redis_connection.get('mobile_%s_time' % phone).decode()
            if times == '3':
                redis_connection.delete('mobile_%s_time' % phone)
                redis_connection.delete('mobile_%s' % phone)
                return Response({"message": "错误次数过多,请重新获取验证码"}, status=http_status.HTTP_400_BAD_REQUEST)
            return Response({"message": "验证码错误"}, status=http_status.HTTP_400_BAD_REQUEST)
        redis_connection.delete("mobile_%s" % phone)
        redis_connection.delete("mobile_%s_time" % phone)
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user_phone)
        user_phone.token = jwt_encode_handler(payload)
        return JsonResponse({
            'user_id': user_phone.id,
            'user': user_phone.username,
            'user_head': user_phone.user_head,
            'token': user_phone.token,
        })


class UserAPIView(CreateAPIView):
    """用户注册"""
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer


class UserInfoApiView(APIView):
    # queryset = UserInfo.objects.all()
    # serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        the_id = request.query_params.get('id')
        user = UserInfo.objects.get(id=the_id)
        serializer = UserSerializer(user)
        return JsonResponse({'data': serializer.data, 'status': http_status.HTTP_200_OK})

    def put(self, request, *args, **kwargs):
        request_data = request.data
        the_id = request_data.get('id')
        if the_id:
            try:
                the_user = UserInfo.objects.get(id=the_id)
                serializer = UserSerializer(data=request_data, instance=the_user)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return JsonResponse({
                    "status": http_status.HTTP_200_OK,
                    "message": '保存成功',
                    "results": serializer.data
                })
            except:
                return JsonResponse({
                    "status": 0,
                    "message": '保存失败'
                })
        else:
            return JsonResponse({
                "status": 0,
                "message": '数据格式错误'
            })


class GoodsInfoApiView(GenericAPIView,
                       ListModelMixin,
                       RetrieveModelMixin,
                       UpdateModelMixin, ):
    queryset = GoodsInfo.objects.filter(is_lost=False)
    serializer_class = GoodsModelSerializer
    lookup_field = 'id'
    filter_backends = [LimitFilter, OrderingFilter]

    pagination_class = MyPagination

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)


class GoodsStatusAPiView(APIView):
    pagination_class = MyPagination

    def patch(self, request, *args, **kwargs):
        the_id = request.data.get('id')
        the_status = request.data.get('status')
        goods = GoodsInfo.objects.get(id=the_id)
        goods.status = the_status
        goods.save()
        return JsonResponse({'data': '1', 'message': '修改成功', "status": http_status.HTTP_200_OK})


class UserPasswordApiView(APIView):
    pagination_class = MyPagination

    def patch(self, request, *args, **kwargs):
        # the_id = request.data.get('id')
        the_old_pass = request.data.get('old_password')
        the_new_pass = request.data.get('new_password')
        if not re.match(r'^[0-pa-zA-Z.+*@#]{3,16}$', the_new_pass):
            return JsonResponse({'data': '1', 'message': '修改失败,新密码格式', "status": http_status.HTTP_400_BAD_REQUEST},
                                status=http_status.HTTP_400_BAD_REQUEST)
        user = request.user
        if user.check_password(the_old_pass):
            user.set_password(the_new_pass)
            return JsonResponse({'data': '1', 'message': '修改成功', "status": http_status.HTTP_200_OK})
        else:
            return JsonResponse({'data': '1', 'message': '修改失败,旧密码错误', "status": http_status.HTTP_400_BAD_REQUEST},
                                status=http_status.HTTP_400_BAD_REQUEST)


class Upload(APIView):

    def post(self, request, *args, **kwargs):
        file_name = str(uuid.uuid4()) + '.jpg'
        obj = request.FILES['file']
        file_path = os.path.join('media', 'user_head', file_name)
        f = open(file_path, 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        img_url = "user_head/" + file_name
        return JsonResponse({'data': img_url, "status": http_status.HTTP_200_OK})
