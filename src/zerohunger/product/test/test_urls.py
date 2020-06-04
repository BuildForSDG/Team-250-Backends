from django.urls import reverse, resolve

from rest_framework.test import APITestCase

from product.views import (
    ProduceAPI,
    AddProductAPI,
    ProduceDetailsAPI,
    ProduceEditDelete
)


class TestProduceUrlsCase(APITestCase):
    def test_get_produce_resolves(self):
        url = reverse('products')
        self.assertEquals(resolve(url).func.view_class, ProduceAPI)

    def test_add_produce_resolves(self):
        url = reverse('add-product')
        self.assertEquals(resolve(url).func.view_class, AddProductAPI)

    def test_produce_details_resolves(self):
        url = reverse('detail-product', args=['1'])
        self.assertEquals(resolve(url).func.view_class, ProduceDetailsAPI)

    def test_produce_edit_delete_resolves(self):
        url = reverse('product-edit-delete', args=['1'])
        self.assertEquals(resolve(url).func.view_class, ProduceEditDelete)
