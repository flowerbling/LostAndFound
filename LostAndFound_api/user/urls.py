# coding:utf-8


from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    path('phone/', views.MobileCheckAPIView.as_view()),
    path('username/', views.UsernameCheckAPIView.as_view()),
    path('captcha/', views.CaptchaAPIView.as_view()),
    path('login/', obtain_jwt_token),
    path('register/', views.UserAPIView.as_view()),
    path('change_pass/', views.UserPasswordApiView.as_view()),
    path('send/', views.SendMessageAPIView.as_view()),
    path('phone_login/', views.PhoneLoginAPIView.as_view()),
    path('phone_check/', views.MobileLoginCheckAPIView.as_view()),
    path('userinfo/', views.UserInfoApiView.as_view()),
    path('goods_info/', views.GoodsInfoApiView.as_view()),
    path('goods_status/', views. GoodsStatusAPiView.as_view()),
    path('upload/', views.Upload.as_view()),

]
