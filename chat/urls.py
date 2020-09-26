from django.urls import path
from . import views

urlpatterns = [
    # path('messages/', views.chat_list, name='chat'),
    path('chatlist/', views.chat_list, name='chat_list'),
    path('massagelist/<int:chatid>/', views.massage_list, name='massage_list'),
    path('messages/<int:chatid>', views.add_massage, name='add_massage'),
    path('conversation/', views.create_conversation, name='create_conversation'),
    path('lastlogin/', views.get_lastlogin, name='last_login'),
    path('getid/', views.get_id, name='id'),
]   