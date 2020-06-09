import os

from django.template import loader
from django.core.mail import EmailMessage, send_mail

from knox.models import AuthToken
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from zerohunger.settings import EMAIL_HOST_USER

from .models import User
from .serializers import (
    CustomerSerializer,
    FarmerSerializer,
    LoginSerializer,
    UserSerializer)


def send_email(user):
    directory_path = os.path.dirname(__file__)
    file_path = os.path.join(directory_path, 'templates/welcome.html')
    html_message = loader.render_to_string(
            file_path,
            {
                'last_name': user.last_name or user.business_name,
                'subject':  'Thank you from Zerohunger',
            }
        )
    subject = 'Welcome to Zerohunger'
    body = "Welcome to Zerohunger"
    recipient = [user.email]
    send_mail(subject, body, EMAIL_HOST_USER, recipient, fail_silently = False, html_message=html_message)

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
        send_email(user)
        return Response({
            "message": "Farmer created succesfully",
            'user': UserSerializer(user).data,
            'business_name': user.business_name,
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
        
        send_email(user)
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
