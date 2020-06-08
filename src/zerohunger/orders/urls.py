from django.urls import path
from .views import OrderAPI, OrderDetailsAPI, OrdersByUserAPI

urlpatterns = [
    path('api/orders', OrderAPI.as_view(), name='orders'),
    path('api/orders/<int:orderId>',
         OrderDetailsAPI.as_view(), name='order-details'),
    path('api/orders/user', OrdersByUserAPI.as_view(), name='user-orders')
]
