from django.urls import path
from .views import OrderAPI

urlpatterns = [
    path('api/order', OrderAPI.as_view(), name='orders')
]
