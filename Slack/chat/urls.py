from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='chat_index'),
    path('room/<slug:slug>/', views.room, name='chat_room'),
    path('api/upload/', views.upload_file, name='chat_file_upload'),
    path('create/', views.create_room, name='create_room'),
]
