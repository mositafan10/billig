from django.urls import path
from . import views

urlpatterns = [
    path('packet/', views.packet_list, name='packet_list'),
    path('packet/update/<int:pk>/', views.update_packet, name='packet_list'),
    path('packet/<int:pk>', views.packet_detail, name='packet_detail'),
    path('packet/<int:pk>/visit/', views.visit_packet, name='packet_visit'),
    path('travel/', views.travel_list, name='travel_list'),
    path('travel/<int:pk>/visit/', views.visit_travel, name='travel_visit'),
    path('packet/<int:pk>/bookmark/', views.bookmark, name='packet_bookmark'),
    # path('travel/<int:pk>', travel_detail, name='travel_detail'),
]