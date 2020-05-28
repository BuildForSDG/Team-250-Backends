from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Farmer
from product.models import Produce


class ProductTestCase(APITestCase):
    url = reverse('products')

    def setUp(self):
        self.user = Farmer.objects.create_farmer(
            email="davinci@gmail.com",
            phone_number="08075985865",
            business_name="Davinci Foods",
            password="Some_very_strong_password"
        )
        self.token = AuthToken.objects.create(self.user)[1]
        self.api_aunthenticate()
        self.produce1 = Produce.objects.create(
            name='Nigerian Rice',
            price=10000,
            farmer_id=self.user,
            description='Best Rice in the universe',
            quantity=20,
            product_img='https://res.cloudinary.com/kayode/image/upload/'
            'v1589264758/unhns7pnrpcjfkifdfgd.jpg'
        )

    def api_aunthenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_produce_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['message'], 'success')
        self.assertEquals(self.produce1.name,
                          response.data['data']['products'][0]['name'])
