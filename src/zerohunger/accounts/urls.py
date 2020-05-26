from django.urls import path
from .views import CustomerRegView, UserLogin, FarmerRegView, WelcomeView


urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome'),
    path('api/auth/signup/farmer', FarmerRegView.as_view(), name='farmer'),
    path('api/auth/signup/customer',
         CustomerRegView.as_view(),  name='customer'),
    path('api/auth/login', UserLogin.as_view(),  name='login')
]
