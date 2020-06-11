from datetime import datetime

from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .helper import get_date
from .models import Orders, ItemsOrdered
from .permissions import IsOwner
from .serializers import OrderSerializer, ItemOrderedSerializer
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
        amount_paid = request.data['amountPaid']
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
        if amount_paid < amount_due:
            return Response({
                'message': 'Amount paid is lower than total of menu purchased '
            }, status=status.HTTP_400_BAD_REQUEST)
        order = Orders.objects.create(
            customer_id=customer_id,
            amount_due=amount_due,
            amount_paid=amount_paid,
            has_paid=True
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


class OrdersByUserAPI(generics.ListAPIView):
    queryset = Orders
    serializer_class = OrderSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner
    ]

    def get(self, request):
        user = request.user
        orders_by_user = Orders.objects.filter(customer_id=user)

        return Response({
            'message': 'success',
            'orders': OrderSerializer(orders_by_user, many=True).data
        })


class DailySalesAPI(generics.GenericAPIView):
    """
      get:
      Return a list of all the sales for a particular Vendor.
        ordering from last to first instance
    """
    queryset = ItemsOrdered.objects.all()
    serializer_class = ItemOrderedSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        user = request.user
        today = datetime.now()
        todays_date = today.date()
        query = ItemsOrdered.objects.filter(
            models.Q(
                orders__has_paid=True
            ) & models.Q(dateTimeCreated=todays_date) & models.Q(
                produce__farmer_id=user))
        prices = []

        for item in query:
            prices.append(item.produce.price)
        total_sales = sum(prices)
        return Response({
            'message': 'success',
            'totalSales': total_sales,
            'itemOrdered': ItemOrderedSerializer(query, many=True).data
        })


class SalesReportAPI(generics.GenericAPIView):
    """
      get:
      Return a list of all the sales for a particular Farmer.
        ordering from last to first instance
    """
    queryset = ItemsOrdered.objects.all()
    serializer_class = ItemOrderedSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        user = request.user
        days = request.data['days']
        use_date = get_date(days)
        query = ItemsOrdered.objects.filter(
            models.Q(
                orders__has_paid=True)
            & models.Q(dateTimeCreated__gte=use_date)
            & models.Q(produce__farmer_id=user)
        )
        prices = []

        for item in query:
            prices.append(item.produce.price)
        total_sales = sum(prices)
        return Response({
            'message': 'success',
            'totalSales': total_sales
        })
