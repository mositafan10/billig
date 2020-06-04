from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.chat_list, name='chat'),

]   