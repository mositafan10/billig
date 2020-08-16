from django.urls import path
from . import views

urlpatterns = [
    # path('packet/update/<int:slug>/', views.update_packet, name='packet_list'),
    path('packet/', views.packet_list, name='packet_list'),
    path('packet/<int:slug>/', views.packet_detail, name='packet_detail'),
    path('packet/<int:slug>/visit/', views.visit_packet, name='packet_visit'),
    path('packet/bookmark/<int:slug>/', views.bookmark, name='bookmark'),
    path('travel/', views.travel_add, name='travel_add'),
    path('travel/<int:pk>/', views.travel_detail, name='travel'),
    path('travellist/', views.travel_user_list, name='travel_user_list'),
    path('travel/<int:slug>/visit/', views.visit_travel, name='travel_visit'),
    path('upload/', views.upload_file),
    path('offer/<int:slug>/', views.offer_list, name='offer_packet_list'),
    path('offer/', views.offer, name='create_offer'),
    path('user_packet/', views.packet_list_user, name='packet_list_user'),
    path('get_picture/<int:pk>/', views.get_picture, name='get_picture'),
    path('getuseroffer/', views.get_user_offer, name='get_user_offer'),
]