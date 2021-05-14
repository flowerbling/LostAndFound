# coding:utf-8
from django.urls import path
from index import views

urlpatterns = [
    path('nav/', views.NavListApiView.as_view()),
    path('foot/', views.FootListApiView.as_view()),
]
