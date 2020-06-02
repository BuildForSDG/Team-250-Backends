from django.urls import reverse, resolve

from rest_framework.test import APITestCase

from orders.views import OrderAPI


class AccountUrlsTestCase(APITestCase):
    def test_order_resolves(self):
        url = reverse('orders')
        self.assertEquals(resolve(url).func.view_class, OrderAPI)
