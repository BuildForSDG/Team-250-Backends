from rest_framework import generics
from rest_framework.response import Response

from .models import Produce
from .serializers import ProduceListSerializer


class ProduceAPI(generics.ListCreateAPIView):
    queryset = Produce.objects.all()
    serializer_class = ProduceListSerializer

    def get(self, request):
        produce = self.get_queryset()

        return Response({
            'message': 'success',
            'data': {
                'products': ProduceListSerializer(produce, many=True).data
            }
        })
