from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Farmer


class AccountViewTestCase(APITestCase):
    def test_welcome(self):
        url = reverse('welcome')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_welcome_invalid(self):
        url = reverse('welcome')
        response = self.client.post(url, {})
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_farmer_registration(self):
        url = reverse('farmer')
        data = {
            "email": "testcase@test.com",
            "password": "some_strong_password",
            "business_name": "Test Case",
            "phone_number": "1234567899",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_farmer_invalid_registration(self):
        url = reverse('farmer')
        data = {
            "email": "",
            "password": "some_strong_password",
            "business_name": "Test Case",
            "phone_number": "1234567899",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_registration(self):
        url = reverse('customer')
        data = {
            "email": "testcase@test.com",
            "password": "some_strong_password",
            "first_name": "Test Case",
            "last_name": "Test Case",
            "phone_number": "1234567899",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_customer_invalid_registration(self):
        url = reverse('customer')
        data = {
            "email": "",
            "password": "some_strong_password",
            "first_name": "Test Case",
            "last_name": "Test Case",
            "phone_number": "1234567899",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        Farmer.objects.create_farmer(
            email="davin@gmail.com",
            phone_number="08075985865",
            business_name="Davinci 007 Foods",
            password="Some_very_strong_password"
        )
        url = reverse('login')
        data = {
            "email": "davin@gmail.com",
            "password": "Some_very_strong_password",
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
