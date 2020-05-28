from django.urls import path
from .views import ProduceAPI, AddProductAPI

urlpatterns = [
    path('api/products', ProduceAPI.as_view(), name='products'),
    path('api/products/add', AddProductAPI.as_view(), name='add-product'),
]
