from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.DashboardHome, name='DashboardHome'),
    path('<str:slug>', views.DashboardPost, name='DashboardPost'),
]