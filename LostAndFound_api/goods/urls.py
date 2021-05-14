# coding:utf-8

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from goods import views

urlpatterns = [
    path('lost_info/', views.GoodsAPIView.as_view()),
    path('pick_info/', views.PickGoodsAPIView.as_view()),
    path('upload/', views.Upload.as_view()),
    path('images/', views.Images.as_view()),
    path('goods_message/', views.GoodsMessageApiView.as_view()),
]
