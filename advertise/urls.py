from django.urls import path
from . import views

urlpatterns = [
    path('packets/', views.packet_add, name='packet_add'),
    path('packets/<str:country>/', views.packet_list, name='packet_list'),
    path('packet/<str:slug>/', views.packet_edit, name='packet_detail'),
    path('bookmarks/<str:slug>/', views.bookmark, name='bookmark'),
    path('bookmarks/', views.bookmark_list, name='bookmark_list'),
    path('travel/', views.travel_add, name='travel_add'),
    path('travel/<str:pk>/', views.travel_detail, name='travel'),
    path('travels/', views.travel_user_list, name='travel_user_list'),
    path('upload/', views.upload_file),
    path('offer/update/', views.offer_update, name='offer_update'),
    path('offers/<str:slug>/', views.offer_list, name='offer_packet_list'),
    path('offer/<str:slug>/', views.offer_delete, name='offer_delete'),
    path('offer/', views.offer, name='create_offer'),
    path('user_packet/', views.packet_list_user, name='packet_list_user'),
    path('get_picture/<str:slug>/', views.get_picture, name='get_picture'),
    path('getuseroffer/', views.get_user_offer, name='get_user_offer'),
    path('categoryList/<int:level>', views.category_list, name='category-list'),
]