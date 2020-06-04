from rest_framework.test import APITestCase
from orders.serializers import ItemOrderedSerializer, OrderSerializer


class OrdersTestCase(APITestCase):
    def test_item_ordered_serialiazer(self):
        data = {
            "menu": 2,
            "quantity": 1
        }
        serializer = ItemOrderedSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_item_ordered_serialiazer_invalid(self):
        data = {
            "menu": 2,
            "quantity": ""
        }
        serializer = ItemOrderedSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_post_order_serializer(self):
        data = {
            "customer_id": 1,
            "amount_due": 2000,
            "items_ordered": [{'produce': 1, 'quantity': 3}],
            "dateAndTimeOfOrder": "2020-06-01T19:05:01.284988Z",
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_post_order_invalid_serializer(self):
        data = {
            "customer_id": 1,
            "amount_due": "",
            "items_ordered": [{'produce': 1, 'quantity': 3}],
            "dateAndTimeOfOrder": "2020-06-01T19:05:01.284988Z",
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
