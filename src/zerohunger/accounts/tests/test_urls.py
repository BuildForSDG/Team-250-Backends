from django.urls import reverse, resolve

from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Customer, User, Farmer
from accounts.serializers import CustomerSerializer, LoginSerializer, FarmerSerializer
from accounts.views import FarmerRegView, CustomerRegView, UserLogin, WelcomeView


class TestUrlsCase(APITestCase):
    def test_welcome_resolves(self):
        url = reverse('welcome')
        self.assertEquals(resolve(url).func.view_class, WelcomeView)

    def test_create_farmer_resolves(self):
        url = reverse('farmer')
        self.assertEquals(resolve(url).func.view_class, FarmerRegView)

    def test_create_customer_resolves(self):
        url = reverse('customer')
        self.assertEquals(resolve(url).func.view_class, CustomerRegView)

    def test_login_user_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, UserLogin)
