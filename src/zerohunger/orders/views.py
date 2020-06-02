from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Orders, ItemsOrdered
from .serializers import OrderSerializer
from product.models import Produce

# Create your views here.


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
