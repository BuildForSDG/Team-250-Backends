from django.urls import path
from .views import (
    OrderAPI,
    OrderDetailsAPI,
    OrdersByUserAPI,
    DailySalesAPI,
    SalesReportAPI
)

urlpatterns = [
    path('api/orders', OrderAPI.as_view(), name='orders'),
    path('api/orders/<int:orderId>',
         OrderDetailsAPI.as_view(), name='order-details'),
    path('api/orders/user', OrdersByUserAPI.as_view(), name='user-orders'),
    path('api/sales/daily', DailySalesAPI.as_view(), name='daily-sales'),
    path('api/sales', SalesReportAPI.as_view(), name='sales')
]
