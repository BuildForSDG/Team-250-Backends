from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Farmer, Customer, User


class FarmerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    business_name = serializers.CharField()
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = Farmer
        fields = [
            'id',
            'email',
            'phone_number',
            'business_name',
            'password'
        ]

    def create(self, validated_data):
        return Farmer.objects.create_farmer(**validated_data)


class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = Customer
        fields = [
            'id',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'password'
        ]

    def create(self, validated_data):
        return Customer.objects.create_customer(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )

        try:
            userObj = Farmer.objects.get(email=user.email)
        except Farmer.DoesNotExist:  # pragma: no cover
            userObj = None
        try:  # pragma: no cover
            if userObj is None:
                userObj = Customer.objects.get(
                    email=user.email)
        except Customer.DoesNotExist:  # pragma: no cover
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )

        if not user.is_active:  # pragma: no cover
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'email': user.email,
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'isFarmer']
