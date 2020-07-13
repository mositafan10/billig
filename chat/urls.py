from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.chat_list, name='chat'),
    path('getid/', views.get_id, name='id'),
]   