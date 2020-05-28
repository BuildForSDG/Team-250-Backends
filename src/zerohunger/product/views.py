from rest_framework import generics, status, permissions
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
import cloudinary.uploader

from .models import Produce
from .permissions import IsFarmerOrReadOnly
from .serializers import ProduceListSerializer


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
        except:  # noqa: E722
            return Response({
                'message': 'error uploading to cloudinary, '
                'Ensure image is attached to the request'
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
