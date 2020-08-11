from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.chat_list, name='chat'),
    path('getid/', views.get_id, name='id'),
    path('chatlist/', views.chat_list, name='chat_list'),
    path('massagelist/<int:chatid>/', views.massage_list, name='massage_list'),
    path('conversation/', views.create_conversation, name='create_conversation'),
    path('message/add/', views.add_massage, name='add_massage'),
]   