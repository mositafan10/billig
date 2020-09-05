from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send, name='send'),
    path('verify/', views.verify, name='verify'),
    path('list/', views.transactions_list, name='transaction_list'),
]