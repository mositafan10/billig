from django.urls import path, include
from django.contrib import admin
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signup/complete/', views.signup_complete, name="signup_complete"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('login/reset_password/', views.reset_password, name="reset_password"),
    path('users/profile/', views.ProfileListCreateView.as_view(), name="profile"),
    path('users/profile/<int:pk>/', views.user_profile, name="profile_detail"),
    path('users/profile/pr/<int:pk>/', views.user_profile_private, name="profile_detail"),
    path('users/', views.UserList.as_view(), name="users"),
    path('users/<int:pk>/', views.UserDetail.as_view(), name="users_detail"),
    path('users/update/', views.update_user, name="update_user"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('countries/', views.country_list, name='country_list'),
    path('cities/<int:pk>/', views.city_list, name='city_list'),
    path('resetpassword/', views.reset_password, name="reset_password"),
    path('confirmresetpassword/', views.confirm_reset_password, name="confirm_reset_password"),
    path('upload/', views.upload_file, name="upload_file"),
    path('rating/', views.rating, name="rate_user"),
    path('comments/<str:pk>', views.comment, name="get_user_comment"),
    path('changepassword/', views.change_password, name="change_password"),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('userinfo/', views.get_user_info, name='user_info'),
    path('socials/', views.social, name='social'),
    path('socials/<int:pk>', views.social_pub, name='social'),
    path('social/<int:pk>', views.social_delete, name='social_delete'),
]