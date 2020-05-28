# Generated by Django 3.0.6 on 2020-05-28 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200528_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(
                default=True,
                help_text='Designates whether this user should be '
                'treated as active. Unselect this instead of '
                ' deleting accounts.', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(
                default=False,
                help_text='Designates whether the user can log '
                ' into this admin site.', verbose_name='staff status'
            ),
        ),
    ]
