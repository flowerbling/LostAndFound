from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from index.models import *
from index.serializers import *


class NavListApiView(ListAPIView):
    queryset = Nav.objects.filter(type=0).order_by("orders")
    serializer_class = NavModelSerializer


class FootListApiView(ListAPIView):
    queryset = Nav.objects.filter(type=1).order_by("orders")
    serializer_class = NavModelSerializer
