from rest_framework.test import APITestCase
from rest_framework import serializers

from accounts.serializers import (
    FarmerSerializer,
    CustomerSerializer,
    LoginSerializer
)
from accounts.models import Farmer, Customer, User


class TestModelCase(APITestCase):
    def test_valid_user_model(self):
        user = User.objects.create(
            email='nana@email.com',
            password='password123456'
        )

        self.assertEquals(user.email, 'nana@email.com')


class TestAccountsSerializer(APITestCase):
    def test_valid_farmer_serializer(self):
        data = {
            "email": "abbeyunique@gmail.com",
            "phone_number": "09076096533",
            "business_name": "logba",
            "password": "politicalnonsense"
        }

        serializer = FarmerSerializer(data=data)
        user = serializer.create(data)
        self.assertTrue(serializer.is_valid())
        self.assertEquals(user.email, data['email'])

    def test_invalidvalid_farmer_serializer(self):
        data = {
            "email": "",
            "phone_number": "09076096533",
            "business_name": "logba",
            "password": ""
        }

        serializer = FarmerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_valid_customer_serializer(self):
        data = {
            "email": "abbeyunique@gmail.com",
            "phone_number": "09076096533",
            "first_name": "logba",
            "last_name": "logba",
            "password": "politicalnonsense"
        }

        serializer = CustomerSerializer(data=data)
        user = serializer.create(data)
        self.assertEquals(user.email, data['email'])

    def test_invalid_customer_serializer(self):
        data = {
            "email": "",
            "phone_number": "09076096533",
            "first_name": "logba",
            "last_name": "logba",
            "password": ""
        }

        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_login_serializer_valid(self):
        user_data = {
            "email": "dummy@test.com",
            "phone_number": "0405894578",
            "password": "oluwanisola",
            "business_name": "Lade Foods"
        }
        user_two = Customer.objects.create_customer(
            email='baba@test.com',
            first_name=user_data['business_name'],
            last_name=user_data['business_name'],
            password=user_data['password'],
            phone_number=user_data['phone_number']
        )
        user_two.is_active = False
        user_two.save()

        Farmer.objects.create_farmer(
            email=user_data['email'],
            business_name=user_data['business_name'],
            password=user_data['password'],
            phone_number=user_data['phone_number']
        )
        valid_data = {
            "email": "dummy@test.com",
            "password": "oluwanisola",
        }
        deactivated_user = {
            "email": "baba@test.com",
            "password": "oluwanisola",
        }
        invalid_user = {
            "email": "duy@test.com",
            "password": "oluwanisola",
        }
        serializer = LoginSerializer()
        self.assertTrue(serializer.validate(valid_data))
        try:
            serializer.validate(invalid_user)
        except serializers.ValidationError as c:
            self.assertRaisesMessage(
                c, 'A user with this email and '
                'password is not found.', code='invalid')
        try:
            serializer.validate(deactivated_user)
        except serializers.ValidationError as c:
            self.assertRaisesMessage(
                c, 'This user has been deactivated.')

    def test_login_serializer_invalid(self):
        data = {}
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
