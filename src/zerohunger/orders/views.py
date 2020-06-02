from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .models import Orders, ItemsOrdered
from .permissions import IsOwner
from .serializers import OrderSerializer

from product.models import Produce


class OrderAPI(generics.ListCreateAPIView):
    queryset = Orders
    serializer_class = OrderSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):
        customer_id = request.user
        items_ordered = request.data['items']
        amount_due = 0
        for item in items_ordered:
            produce = Produce.objects.get(id=item['produceId'])
            if item['quantity'] > produce.quantity:
                return Response({
                    'message': 'item in stock is lower than quantity requested'
                }, status=status.HTTP_400_BAD_REQUEST)
            produce.quantity -= item['quantity']
            produce.save()
            amount_due += produce.price * item['quantity']

        order = Orders.objects.create(
            customer_id=customer_id,
            amount_due=amount_due
        )
        for item in items_ordered:
            produce = Produce.objects.get(id=item['produceId'])
            ItemsOrdered.objects.create(
                orders=order, produce=produce, quantity=item['quantity'])
        return Response({
            "message": "success",
            "order": OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)


class OrderDetailsAPI(generics.RetrieveAPIView):
    queryset = Orders
    serializer_class = OrderSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner
    ]

    def get_object(self, id):
        id = int(id)
        obj = get_object_or_404(Orders, id=id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, orderId):
        order = self.get_object(orderId)
        return Response({
            'message': 'success',
            'order': OrderSerializer(order).data
        })
