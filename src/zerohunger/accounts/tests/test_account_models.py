from rest_framework.test import APITestCase

from accounts.models import Farmer, Customer, User


class AccountModelsTestCase(APITestCase):
    def test_farmer_model(self):
        farmer = Farmer.objects.create_farmer(
            email="davinci0072@gmail.com",
            phone_number="08075985865",
            business_name="Davinci 007 Foods",
            password="Some_very_strong_password",
            location="Oyo"
        )
        self.assertEquals(str(farmer), 'davinci0072@gmail.com')

    def test_customer_model(self):
        customer = Customer.objects.create_customer(
            email="davinci0073@gmail.com",
            phone_number="08075985865",
            first_name="Davinci 007 Foods",
            last_name="Davinci 007 Foods",
            password="Some_very_strong_password",
            location="Oyo"
        )
        self.assertEquals(str(customer), 'davinci0073@gmail.com')

    def test_user_model(self):
        user = User.objects.create(
            email="davinci0075@gmail.com",
            password="Some_very_strong_password"
        )
        self.assertEquals(str(user), 'davinci0075@gmail.com')
