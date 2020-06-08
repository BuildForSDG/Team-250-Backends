from rest_framework.test import APITestCase
from product.models import Produce
from accounts.models import Farmer


class TestModelCase(APITestCase):
    def setUp(self):
        self.user = Farmer.objects.create_farmer(
            email="davinci@gmail.com",
            phone_number="08075985865",
            business_name="Davinci Foods",
            password="Some_very_strong_password",
            location="Oyo"
        )

    def test_product_str(self):
        product = Produce.objects.create(
            name='Nigerian Beans',
            price=10000,
            farmer_id=self.user,
            description='Best Rice in the universe',
            quantity=20,
            product_img='https://res.cloudinary.com/kayode/image/upload/'
            'v1589264758/unhns7pnrpcjfkifdfgd.jpg'
        )

        p = str(product)
        self.assertEquals(p, 'Nigerian Beans')
