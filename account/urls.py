from django.urls import path, include
from django.contrib import admin
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('login/reset_password/', views.reset_password, name="reset_password"),
    path('users/profile/', views.ProfileListCreateView.as_view(), name="profile"),
    path('users/profile/<int:pk>/', views.user_profile, name="profile_detail"),
    path('users/', views.UserList.as_view(), name="users"),
    path('users/<int:pk>/', views.UserDetail.as_view(), name="users_detail"),
    path('users/update/', views.update_user, name="update_user"),
    path('social/<int:pk>/', views.social_detail, name="social"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('countries/', views.country_list, name='country_list'),
    path('cities/', views.city_list, name='city_list'),
    path('checktoken/', views.CheckAuth.as_view()),
    path('resetpassword/', views.reset_password, name="reset_password"),
    path('confirmresetpassword/', views.confirm_reset_password, name="confirm_reset_password"),
    path('friend/', views.friend_request, name="friend_request"),
    path('friend_list/', views.friend_list, name="friend_list"),
    # path('signup/user/', views.create_user, name="create_user"),
]