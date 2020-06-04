from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='blog'),
    path('posts/', views.post_list),
    path('posts/<int:pk>/', views.post_detail, name='post detail'),
    path('posts/<int:pk>/like/', views.like_post),
    path('posts/<int:pk>/dislike/', views.dislike_post),
    path('posts/<int:pk>/view/', views.visit_count),
    path('posts/<int:pk>/score/', views.score),
]