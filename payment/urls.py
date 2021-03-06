from django.urls import path

from . import views

urlpatterns = [
    path('send/', views.send, name='send'),
    path('verify/', views.verify, name='verify'),
    path('list/', views.transactions_list, name='transaction_list'),
    path('cashoutList/', views.cashout_list, name='cashout_list'),
    path('paytraveler/', views.pay_to_traveler, name='pay_to_traveler'),
    path('accounts/', views.accounts, name='accounts'),
]