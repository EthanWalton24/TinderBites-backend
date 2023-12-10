from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('auth/register', views.CreateUserAPIView.as_view(), name='auth_user_register'),
    path('auth/login', obtain_auth_token, name='auth_user_login'),
    path('auth/logout', views.LogoutUserAPIView.as_view(), name='auth_user_logout'),

    path('group/update/address', views.UpdateAddressView.as_view(), name='update_address'),
    
    path('list_users', views.ListUsers.as_view(), name='list_users'),
    path('getPlaces', views.GetPlaces.as_view(), name='get_places'),
]