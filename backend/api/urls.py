from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('auth/register', views.CreateUserAPIView.as_view(), name='auth_user_register'),
    path('auth/login', obtain_auth_token, name='auth_user_login'),
    path('auth/logout', views.LogoutUserAPIView.as_view(), name='auth_user_logout'),
    
    path('list_users', views.ListUsers.as_view(), name='list_users'),
    path('getPlaces', views.GetPlaces.as_view(), name='get_places'),
    path('Settings', views.Settings.as_view(), name='settings'),
    path('Profile', views.Profile.as_view(), name='profile'),
]