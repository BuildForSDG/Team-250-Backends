import os

from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Farmer, Customer
from product.models import Produce


class ProductTestCase(APITestCase):
    list_url = reverse('products')
    add_url = reverse('add-product')
    directory_path = os.path.dirname(__file__)
    file_path = os.path.join(directory_path, 'img.jpg')

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
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['message'], 'success')
        self.assertEquals(self.produce1.name,
                          response.data['products'][0]['name'])

    def test_produce_add(self):
        data = {
            "name": "aaaaaaaaaaaaaa",
            "price": 2000,
            "description": "aaaaaaaaaaaaaa",
            "quantity": 20,
            "product_img": self.file_path
        }

        response = self.client.post(self.add_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data
                         ['product']['name'], data['name'])

    def test_produce_add_fail(self):
        data = {
            "name": "aaaaaaaaaaaaaa",
            "price": 2000,
            "description": "aaaaaaaaaaaaaa",
            "quantity": 20,
            "product_img": ''
        }

        response = self.client.post(self.add_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_produce_add_unpermitted(self):
        user = Customer.objects.create_customer(
            email="user2@gmail.com",
            phone_number="08075985865",
            first_name="User",
            last_name="Two",
            password="Some_very_strong_password"
        )

        token = AuthToken.objects.create(user)[1]
        self.user = user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        data = {
            "name": "aaaaaaaaaaaaaa",
            "price": 2000,
            "description": "aaaaaaaaaaaaaa",
            "quantity": 20,
            "product_img": ''
        }
        response = self.client.post(self.add_url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        message = 'Only a Farmer can perform this operation'
        self.assertEquals(response.data['detail'], message)
        count = Produce.objects.count()
        self.assertEqual(count, 1)

    def test_produce_create_unauthorize_user(self):
        data = {
            "name": "aaaaaaaaaaaaaa",
            "price": 2000,
            "description": "aaaaaaaaaaaaaa",
            "quantity": 20,
            "product_img": ''
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(self.add_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        count = Produce.objects.count()
        self.assertEqual(count, 1)
    # test menu details retrieve by id valid user

    def test_product_details_retrieve_valid(self):
        response = self.client.get(reverse('detail-product', args=['1']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.produce1.name, response.data['product']['name'])

    def test_product_details_retrieve_invalid(self):
        response = self.client.get(reverse('detail-product', args=['2']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
