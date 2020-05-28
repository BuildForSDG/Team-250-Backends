from django.urls import path
from .views import ProduceAPI

urlpatterns = [
    path('api/products', ProduceAPI.as_view(), name='products')
]
