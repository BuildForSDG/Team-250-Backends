from django.urls import path
from .views import ProduceAPI, AddProductAPI, ProduceDetailsAPI

urlpatterns = [
    path('api/products', ProduceAPI.as_view(), name='products'),
    path('api/product/add', AddProductAPI.as_view(), name='add-product'),
    path('api/products/<int:id>',
         ProduceDetailsAPI.as_view(), name='detail-product'),
]
