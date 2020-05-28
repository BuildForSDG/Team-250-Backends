from rest_framework import serializers
from .models import Produce
from cloudinary.forms import CloudinaryFileField
from accounts.serializers import FarmerSerializer


class ProduceListSerializer(serializers.ModelSerializer):
    product_img = CloudinaryFileField(
        options={
            'crop': 'thumb',
            'width': 200,
            'height': 200
        }
    )
    farmerId = FarmerSerializer(read_only=True)

    class Meta:
        model = Produce
        fields = '__all__'
