from rest_framework.test import APITestCase
from product.serializers import ProduceListSerializer, ProduceEditSerializer
from accounts.models import Farmer


class TestProductSerializer(APITestCase):
    def setUp(self):
        self.user = Farmer.objects.create_farmer(
            email="davinci@gmail.com",
            phone_number="08075985865",
            business_name="Davinci Foods",
            password="Some_very_strong_password",
            location="Oyo"
        )

    def test_valid_product_serializers(self):
        data = {
            "name": 'Nigerian Rice',
            "price":  10000,
            "farmer_id": 1,
            "description": 'Best Rice in the universe',
            "quantity": 20,
            "product_img": 'https://res.cloudinary.com/kayode/image/upload/'
            'v1589264758/unhns7pnrpcjfkifdfgd.jpg'
        }

        serializer = ProduceListSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_product_serializers(self):
        data = {
            "name": '',
            "price":  10000,
            "farmer_id": 1,
            "description": 'Best Rice in the universe',
            "quantity": 20,
            "product_img": 'https://res.cloudinary.com/kayode/image/upload/'
            'v1589264758/unhns7pnrpcjfkifdfgd.jpg'
        }
        serializer = ProduceListSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_valid_edit_product_serializers(self):
        data = {
            "name": 'Nigerian Rice',
            "price":  10000,
            "farmer_id": 1,
            "description": 'Best Rice in the universe',
            "quantity": 20,
            "product_img": 'https://res.cloudinary.com/kayode/image/upload/'
            'v1589264758/unhns7pnrpcjfkifdfgd.jpg'
        }

        serializer = ProduceEditSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_valid_edit_product_serializers(self):
        data = {
            "name": '',
            "price":  10000,
        }

        serializer = ProduceEditSerializer(data=data)
        self.assertFalse(serializer.is_valid())
