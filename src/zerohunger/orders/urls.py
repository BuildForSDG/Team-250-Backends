from django.urls import path
from .views import OrderAPI, OrderDetailsAPI

urlpatterns = [
    path('api/orders', OrderAPI.as_view(), name='orders'),
    path('api/orders/<int:orderId>',
         OrderDetailsAPI.as_view(), name='order-details'),
]
