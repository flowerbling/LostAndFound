import os
import uuid

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from goods.MyFilter import LimitFilter
from goods.models import GoodsInfo, GoodsImage
from goods.pagination import MyPagination
from goods.serializers import GoodsModelSerializer, GoodsImageModelSerializer, GoodsMessageModelSerializer


class GoodsAPIView(GenericAPIView,
                   ListModelMixin,
                   RetrieveModelMixin,
                   CreateModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin):
    queryset = GoodsInfo.objects.filter(is_lost=True, status=True).order_by("-id")
    serializer_class = GoodsModelSerializer
    lookup_field = 'id'
    filter_backends = [LimitFilter, OrderingFilter]

    pagination_class = MyPagination

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PickGoodsAPIView(GenericAPIView,
                       ListModelMixin,
                       RetrieveModelMixin,
                       CreateModelMixin,
                       UpdateModelMixin,
                       DestroyModelMixin):
    queryset = GoodsInfo.objects.filter(is_lost=False, status=True).order_by("-id")
    serializer_class = GoodsModelSerializer
    lookup_field = 'id'
    filter_backends = [LimitFilter, OrderingFilter]

    pagination_class = MyPagination

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GoodsMessageApiView(GenericAPIView,
                          ListModelMixin,
                          CreateModelMixin, ):
    permission_classes = [IsAuthenticated]
    queryset = GoodsImage.objects.filter()
    serializer_class = GoodsMessageModelSerializer
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Images(GenericAPIView,
             ListModelMixin,
             CreateModelMixin,
             ):
    permission_classes = [IsAuthenticated]
    queryset = GoodsImage.objects.filter()
    serializer_class = GoodsImageModelSerializer
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Upload(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_name = str(uuid.uuid4()) + '.jpg'
        obj = request.FILES['file']
        file_path = os.path.join('media', 'goods_image', file_name)
        f = open(file_path, 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        img_url = "goods_image/" + file_name
        return JsonResponse({'data': img_url, "status": status.HTTP_200_OK})
