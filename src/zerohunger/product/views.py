from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

import cloudinary.uploader

from .models import Produce
from .permissions import IsFarmerOrReadOnly, IsOwnerOrReadOnly
from .serializers import ProduceListSerializer, ProduceEditSerializer


class ProduceAPI(generics.ListAPIView):
    queryset = Produce.objects.all()
    serializer_class = ProduceListSerializer

    def get(self, request):
        produce = self.get_queryset()

        return Response({
            'message': 'success',
            'products': ProduceListSerializer(produce, many=True).data
        })


class AddProductAPI(generics.CreateAPIView):
    queryset = Produce.objects.all()
    serializer_class = ProduceListSerializer
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )
    permission_classes = [
        permissions.IsAuthenticated,
        IsFarmerOrReadOnly
    ]

    def post(self, request):
        file = request.data.get('product_img')
        try:
            upload_data = cloudinary.uploader.upload(file)
        except cloudinary.exceptions.Error as c:
            return Response({
                'message': 'error uploading to cloudinary, '
                'Ensure image is attached to the request',
                'error': str(c)
            }, status=status.HTTP_400_BAD_REQUEST)

        product_img = upload_data['url']
        farmer_id = request.user
        name = request.data['name']
        price = request.data['price']
        description = request.data['description']
        quantity = request.data['quantity']

        product = Produce.objects.create(
            name=name,
            price=price,
            description=description,
            quantity=quantity,
            farmer_id=farmer_id,
            product_img=product_img
        )

        return Response({
            'message': 'success',
            'product': ProduceListSerializer(product).data
        }, status=status.HTTP_201_CREATED)


class ProduceDetailsAPI(generics.RetrieveAPIView):
    queryset = Produce.objects.all()
    serializer_class = ProduceListSerializer

    def get(self, request, id):
        product = get_object_or_404(Produce, id=id)

        return Response({
            'message': 'success',
            'product': ProduceListSerializer(product).data
        })


class ProduceEditDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produce.objects.all()
    serializer_class = ProduceListSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsFarmerOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_object(self, id):
        id = int(id)
        obj = get_object_or_404(Produce, id=id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, id):
        product = self.get_object(id)

        return Response({
            'message': 'success',
            'product': ProduceListSerializer(product).data
        })

    def put(self, request, id):
        produce = self.get_object(id)

        data = request.data
        serializer = ProduceEditSerializer(produce, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'success',
                'product': serializer.data
            })
        return Response({
            'message': 'error',
            'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
