from django.urls import path
from .views import (
    CustomerRegView, UserLogin, FarmerRegView, welcome, GetUserAPI)
from knox import views as knox_views


urlpatterns = [
    path('', welcome, name='welcome'),
    path('api/auth/signup/farmer', FarmerRegView.as_view(), name='farmer'),
    path('api/auth/signup/customer',
         CustomerRegView.as_view(),  name='customer'),
    path('api/auth/user', GetUserAPI.as_view(), name='user'),
    path('api/auth/login', UserLogin.as_view(),  name='login'),
    path('api/auth/logout', knox_views.LogoutView.as_view(),  name='logout')
]
