from rest_framework import serializers
from .models import Produce
from cloudinary.forms import CloudinaryFileField
from accounts.serializers import UserSerializer


class ProduceListSerializer(serializers.ModelSerializer):
    product_img = CloudinaryFileField(
        options={
            'crop': 'thumb',
            'width': 200,
            'height': 200
        }
    )
    farmerId = UserSerializer(read_only=True)

    class Meta:
        model = Produce
        fields = '__all__'


class ProduceEditSerializer(serializers.ModelSerializer):
    farmer_id = UserSerializer(read_only=True)
    name = serializers.CharField(required=True)
    product_img = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    price = serializers.FloatField(required=False)
    quantity = serializers.IntegerField(required=False)

    class Meta:
        model = Produce
        fields = ['farmer_id', 'name', 'price',
                  'product_img', 'description', 'quantity']


class ProduceSerializer(serializers.ModelSerializer):
    # farmer_id = UserSerializer(read_only=True)

    class Meta:
        model = Produce
        fields = ['name', 'price']
