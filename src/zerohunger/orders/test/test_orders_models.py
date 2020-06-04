from rest_framework.test import APITestCase

from accounts.models import Customer
from orders.models import Orders


class OrderModelTestCase(APITestCase):
    def setUp(self):
        self.user = Customer.objects.create_customer(
            email="user2@gmail.com",
            phone_number="08075985865",
            first_name="User",
            last_name="Two",
            password="Some_very_strong_password"
        )

    def test_orders_model(self):
        order = Orders.objects.create(
            customer_id=self.user,
            amount_due=10000,
            amount_paid=10003
        )
        amount_outs = order.amount_outstanding
        oust = order.amount_due - order.amount_paid
        self.assertEquals(amount_outs, oust)
