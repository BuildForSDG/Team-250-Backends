# Generated by Django 3.0.6 on 2020-06-08 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='amount_paid',
            field=models.FloatField(default=10000),
            preserve_default=False,
        ),
    ]
