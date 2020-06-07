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
            password="Some_very_strong_password",
            location="Oyo"
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

        self.assertEquals(self.produce1.name,
                          response.data['results'][0]['name'])

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

    def test_produce_add_not_safe(self):
        data = {
            "name": "aaaaaaaaaaaaaa",
            "price": 2000,
            "description": "aaaaaaaaaaaaaa",
            "quantity": 20,
            "product_img": self.file_path
        }

        response = self.client.put(self.add_url, data)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

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
            password="Some_very_strong_password",
            location="Oyo"
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

    def test_produce_add_unpermitted_safe_permissions(self):
        user = Customer.objects.create_customer(
            email="user2@gmail.com",
            phone_number="08075985865",
            first_name="User",
            last_name="Two",
            password="Some_very_strong_password",
            location="Oyo"
        )

        token = AuthToken.objects.create(user)[1]
        self.user = user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.options(self.add_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

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

    def test_product_edit_permitted_owner(self):
        url = reverse('product-edit-delete', args=['2'])
        Produce.objects.create(
            name='Nigerian Beans',
            price=10000,
            farmer_id=self.user,
            description='Best Rice in the universe',
            quantity=20,
            product_img='https://res.cloudinary.com/kayode/image/upload/'
            'v1589264758/unhns7pnrpcjfkifdfgd.jpg'
        )

        data = {
            "name": "product 2",
            "price": 2000,
            "description": "product 2 description"
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data
                         ['product']['name'], data['name'])

    def test_product_edit_unpermitted_owner(self):
        user = Farmer.objects.create_farmer(
            email="user2@gmail.com",
            phone_number="08075985865",
            business_name="User",
            password="Some_very_strong_password",
            location="Oyo"
        )
        token = AuthToken.objects.create(user)[1]
        self.user = user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        url = reverse('product-edit-delete', args=['1'])
        data = {
            "name": "product 2",
            "price": 2000,
            "description": "product 2 description"
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_detail_update_by_customer_user(self):

        user = Customer.objects.create_customer(
            email="user3@gmail.com",
            phone_number="08075985865",
            first_name="User",
            last_name="Two",
            password="Some_very_strong_password",
            location="Oyo"
        )

        token = AuthToken.objects.create(user)[1]
        self.user = user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        url = reverse('product-edit-delete', args=['1'])
        data = {
            "name": "Amala Delicious",
            "description": "Amala Sumptuos",
            "quantity": 2
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_details_retrieve_update_valid(self):
        user = Customer.objects.create_customer(
            email="user3@gmail.com",
            phone_number="08075985865",
            first_name="User",
            last_name="Two",
            password="Some_very_strong_password",
            location="Oyo"
        )

        token = AuthToken.objects.create(user)[1]
        self.user = user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        url = reverse('product-edit-delete', args=['1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.produce1.name, response.data['product']['name'])

    def test_product_details_update_invalid(self):
        url = reverse('product-edit-delete', args=['2'])
        Produce.objects.create(
            name='Nigerian Beans pp',
            price=10000,
            farmer_id=self.user,
            description='Best Rice in the universe',
            quantity=20,
            product_img='https://res.cloudinary.com/kayode/image/upload/'
            'v1589264758/unhns7pnrpcjfkifdfgd.jpg'
        )

        data = {
            "name": "",
            "price": 2000,
            "description": "product 2 description"
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_detail_delete_by_permitted_owner(self):
        url = reverse('product-edit-delete', args=['2'])
        Produce.objects.create(
            name='Nigerian Beans pp',
            price=10000,
            farmer_id=self.user,
            description='Best Rice in the universe',
            quantity=20,
            product_img='https://res.cloudinary.com/kayode/image/upload/'
            'v1589264758/unhns7pnrpcjfkifdfgd.jpg'
        )

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_product_detail_delete_by_unpermitted_owner(self):
        url = reverse('product-edit-delete', args=['1'])

        user = Farmer.objects.create_farmer(
            email="user2@gmail.com",
            phone_number="08075985865",
            business_name="User",
            password="Some_very_strong_password",
            location="Oyo"
        )

        token = AuthToken.objects.create(user)[1]
        self.user = user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_produce_detail_delete_by_invalid(self):
        url = reverse('product-edit-delete', args=['2'])
        Produce.objects.create(
            name='Nigerian Beans pp',
            price=10000,
            farmer_id=self.user,
            description='Best Rice in the universe',
            quantity=20,
            product_img='https://res.cloudinary.com/kayode/image/upload/'
            'v1589264758/unhns7pnrpcjfkifdfgd.jpg'
        )
        self.client.force_authenticate(user=None)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_produce_detail_delete_by_customer(self):
        url = reverse('product-edit-delete', args=['1'])
        user = Customer.objects.create_customer(
            email="user2@gmail.com",
            phone_number="08075985865",
            first_name="User",
            last_name="Two",
            password="Some_very_strong_password",
            location="Oyo"
        )

        token = AuthToken.objects.create(user)[1]
        self.user = user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filters(self):
        url = '/api/products/filter?search=nigerian'
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
