from django.urls import path
from . import views

urlpatterns = [
    path('chatlist/', views.chat_list, name='chat_list'),
    path('massagelist/<str:chatid>/', views.massage_list, name='massage_list'),
    path('newMassageList/<str:chatid>/', views.new_massage_list, name='massage_list'),
    path('messages/<str:chatid>', views.add_massage, name='add_massage'),
    path('conversation/', views.create_conversation, name='create_conversation'),
    path('conversation/<str:slug>/', views.conversation, name='conversation'),
    path('lastlogin/', views.get_lastlogin, name='last_login'),
    path('notifications/', views.notification_register, name='notification_register'),
]   