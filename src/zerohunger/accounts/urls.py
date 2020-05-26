from django.urls import path
from .views import CustomerRegView, UserLogin, FarmerRegView, welcome


urlpatterns = [
    path('', welcome, name='welcome'),
    path('api/auth/signup/farmer', FarmerRegView.as_view(), name='farmer'),
    path('api/auth/signup/customer',
         CustomerRegView.as_view(),  name='customer'),
    path('api/auth/login', UserLogin.as_view(),  name='login')
]
