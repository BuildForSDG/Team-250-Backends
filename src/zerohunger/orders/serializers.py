from rest_framework import serializers
from .models import Orders, ItemsOrdered
from accounts.serializers import UserSerializer
from product.serializers import ProduceSerializer


class ItemOrderedSerializer(serializers.ModelSerializer):
    produce = ProduceSerializer(read_only=True)

    class Meta:
        model = ItemsOrdered
        fields = ['produce', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items_ordered = serializers.SerializerMethodField()
    customer_id = UserSerializer(read_only=True)

    class Meta:
        model = Orders
        fields = [
            'id',
            'customer_id',
            'amount_due',
            'amount_paid',
            'amount_outstanding',
            'items_ordered',
            'dateAndTimeOfOrder'
        ]

    def get_items_ordered(self, obj):
        qset = ItemsOrdered.objects.filter(orders=obj)
        return [ItemOrderedSerializer(m).data for m in qset]
