import json

from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Farmer, Customer
from product.models import Produce
from orders.models import Orders, ItemsOrdered


class OrderViewsTestCase(APITestCase):
    url = reverse('orders')

    def setUp(self):
        self.farmer = Farmer.objects.create_farmer(
            email="davinci008@gmail.com",
            phone_number="08075985865",
            business_name="Davinci Foods",
            password="Some_very_strong_password"
        )
        self.produce1 = Produce.objects.create(
            name='Nigerian Rice',
            price=10000,
            farmer_id=self.farmer,
            description='Best Rice in the universe',
            quantity=20,
            product_img='https://res.cloudinary.com/kayode/image/upload/'
            'v1589264758/unhns7pnrpcjfkifdfgd.jpg'
        )
        self.produce2 = Produce.objects.create(
            name='Nigerian Tool',
            price=10000,
            farmer_id=self.farmer,
            description='Best Rice in the universe',
            quantity=20,
            product_img='https://res.cloudinary.com/kayode/image/upload/'
            'v1589264758/unhns7pnrpcjfkifdfgd.jpg'
        )
        self.user = Customer.objects.create_customer(
            email="user2@gmail.com",
            phone_number="08075985865",
            first_name="User",
            last_name="Two",
            password="Some_very_strong_password"
        )
        self.token = AuthToken.objects.create(self.user)[1]
        self.api_aunthenticate()
        self.order = Orders.objects.create(
            customer_id=self.user,
            amount_due=2500
        )
        ItemsOrdered.objects.create(
            orders=self.order, produce=self.produce1, quantity=2)

    def api_aunthenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_post_orders(self):
        data = {
            "items": [
                {
                    "quantity": 1,
                    "produceId": 1
                },
                {
                    "quantity": 2,
                    "produceId": 2
                }
            ]
        }
        parse_data = json.dumps(data)
        response = self.client.post(
            self.url, data=parse_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        count = Orders.objects.count()
        self.assertEqual(count, 2)

    def test_post_unpermitted_user(self):
        data = {
            "items": [
                {
                    "quantity": 3,
                    "produceId": 1
                },
                {
                    "quantity": 2,
                    "produceId": 2
                }
            ]
        }
        parse_data = json.dumps(data)
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.url, data=parse_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        count = Orders.objects.count()
        self.assertEqual(count, 1)

    def test_post_invalid_orders(self):
        data = {
            "items": [
                {
                    "quantity": 23,
                    "produceId": 1
                },
                {
                    "quantity": 2,
                    "produceId": 2
                }
            ]
        }
        parse_data = json.dumps(data)
        response = self.client.post(
            self.url, data=parse_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_details_valid_user(self):
        url = reverse('order-details', args=['1'])

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        test_user = response.data['order']['customer_id']['email']
        self.assertEquals(test_user, self.user.email)

    def test_order_details_unauthorized_user(self):
        url = reverse('order-details', args=['1'])
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_details_unpermitted_user(self):
        url = reverse('order-details', args=['1'])
        user = Customer.objects.create_customer(
            email="user3@gmail.com",
            phone_number="08075985865",
            first_name="User",
            last_name="Two",
            password="Some_very_strong_password"
        )
        token = AuthToken.objects.create(user)[1]
        self.user = user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
