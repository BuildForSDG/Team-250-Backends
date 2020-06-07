from knox.models import AuthToken
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User
from .serializers import (
    CustomerSerializer,
    FarmerSerializer,
    LoginSerializer,
    UserSerializer)


@api_view(['GET'])
def welcome(request):
    if request.method == 'GET':
        return Response('Welcome To Team-250 Zero Hunger Backend')


class FarmerRegView(generics.CreateAPIView):

    serializer_class = FarmerSerializer

    def post(self, request):
        """
        post:
        Create a new Farmer.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)[1]
        return Response({
            "message": "Farmer created succesfully",
            'user': UserSerializer(user).data,
            'token': token
        }, status=status.HTTP_201_CREATED)


class CustomerRegView(generics.CreateAPIView):
    serializer_class = CustomerSerializer

    def post(self, request):
        """
        post:
        Create a new Customer.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)[1]
        return Response({
            "message": "customer created succesfully",
            'user': UserSerializer(user).data,
            'token': token
        }, status=status.HTTP_201_CREATED)


class UserLogin(generics.CreateAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        token = AuthToken.objects.create(user)[1]
        return Response({
            "message": "Login succesfully",
            'user': UserSerializer(user).data,
            'token': token
        }, status=status.HTTP_201_CREATED)


# GET Users API
class GetUserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
