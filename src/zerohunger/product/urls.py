from django.urls import path
from .views import (
    ProduceAPI, AddProductAPI, ProduceDetailsAPI, ProduceEditDelete)

urlpatterns = [
    path('api/products', ProduceAPI.as_view(), name='products'),
    path('api/product/add', AddProductAPI.as_view(), name='add-product'),
    path('api/products/<int:id>',
         ProduceDetailsAPI.as_view(), name='detail-product'),
    path('api/products/details/<int:id>',
         ProduceEditDelete.as_view(), name='product-edit-delete')
]
