# Generated by Django 3.0.6 on 2020-06-01 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='orderStatus',
            new_name='order_status',
        ),
    ]
