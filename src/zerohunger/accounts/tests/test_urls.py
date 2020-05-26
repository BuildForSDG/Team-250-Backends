from django.urls import reverse, resolve

from rest_framework.test import APITestCase
from accounts.views import (
    FarmerRegView,
    CustomerRegView,
    UserLogin,
    welcome
)


class TestUrlsCase(APITestCase):
    def test_welcome_resolves(self):
        url = reverse('welcome')
        self.assertEquals(
            resolve(url).func, welcome)

    def test_create_farmer_resolves(self):
        url = reverse('farmer')
        self.assertEquals(
            resolve(url).func.view_class, FarmerRegView)

    def test_create_customer_resolves(self):
        url = reverse('customer')
        self.assertEquals(
            resolve(url).func.view_class, CustomerRegView)

    def test_login_user_resolves(self):
        url = reverse('login')
        self.assertEquals(
            resolve(url).func.view_class, UserLogin)
