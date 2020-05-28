# Generated by Django 3.0.6 on 2020-05-28 09:51

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Produce',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID')
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Name of the product',
                        max_length=100,
                        verbose_name='Name')
                ),
                (
                    'price',
                    models.FloatField(
                        help_text='Price of the Product (Float)',
                        verbose_name='Price per Bag')
                ),
                (
                    'description',
                    models.TextField(
                        help_text='Product Description (Text Field)',
                        verbose_name='Description of the product')
                ),
                (
                    'quantity',
                    models.IntegerField(
                        help_text='Quantity of Product Available',
                        verbose_name='Quantity Available')
                ),
                (
                    'product_img',
                    cloudinary.models.CloudinaryField(
                        max_length=255,
                        verbose_name='product_image')
                ),
                (
                    'create_date',
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name='Date of Creation')
                ),
                (
                    'farmer_id',
                    models.ForeignKey(
                        help_text='Farmer Id, gotten from request.user',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='farmer_produce',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='Farmer')),
            ],
        ),
    ]
