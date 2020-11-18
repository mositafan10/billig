from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signup/complete/', views.signup_complete, name="signup_complete"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('login/reset_password/', views.reset_password, name="reset_password"),
    path('users/profile/<str:pk>/', views.user_profile, name="profile_detail"),
    path('users/profile/pr/<str:pk>/', views.user_profile_private, name="profile_detail"),
    path('users/update/', views.update_user, name="update_user"),
    path('countries/', views.country_list, name='country_list'),
    path('cities/<int:pk>/', views.city_list, name='city_list'),
    path('resetpassword/', views.reset_password, name="reset_password"),
    path('confirmresetpassword/', views.confirm_reset_password, name="confirm_reset_password"),
    path('upload/', views.upload_file, name="upload_file"),
    path('rating/', views.rating, name="rate_user"),
    path('rate_user_list/<str:user>', views.rate_user_list, name="get_user_comment"),
    path('comments/', views.comment, name="get_user_comment"),
    path('comments_billlig/', views.comments_billlig, name="comments_billlig"),
    path('changepassword/', views.change_password, name="change_password"),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('userinfo/', views.get_user_info, name='user_info'),
    path('socials/', views.social, name='social'),
    path('socials/<str:slug>', views.social_pub, name='social'),
    path('social/<str:slug>', views.social_delete, name='social_delete'),
]