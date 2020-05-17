from django.shortcuts import get_object_or_404, render
from knox.models import AuthToken
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

from .models import User
from .serializers import CustomerSerializer, FarmerSerializer, LoginSerializer

class FarmerRegView(generics.CreateAPIView):
    
  serializer_class = FarmerSerializer

  def post(self, request):
        """
        create:
          Create a new Farmer.
        """  
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token =  AuthToken.objects.create(user)[1]
        return Response({
          "message": "Farmer created succesfully",
          'farmer': serializer.data,
          'token': token
          }, status=status.HTTP_201_CREATED)


class CustomerRegView(generics.CreateAPIView):
  serializer_class = CustomerSerializer

  def post(self, request):
        """
        create:
          Create a new Customer.
        """  
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token =  AuthToken.objects.create(user)[1]
        return Response({
          "message": "customer created succesfully",
          'customer': serializer.data,
          'token': token
          }, status=status.HTTP_201_CREATED)

class UserLogin(generics.CreateAPIView):
  

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        token =  AuthToken.objects.create(user)[1]
        return Response({
          "message": "Login succesfully",
          'user': serializer.data,
          'token': token
          }, status=status.HTTP_201_CREATED)
