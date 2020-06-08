from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager


class FarmerManager(BaseUserManager):
    def create_farmer(
        self,
        email,
        phone_number,
        business_name,
        location,
        password=None
    ):
        if email is None:
            raise TypeError(
                'Users must have an email address.')  # pragma: no cover
        farmer = Farmer(
            email=self.normalize_email(email),
            phone_number=phone_number,
            business_name=business_name,
            location=location,
            isFarmer=True
        )
        farmer.set_password(password)
        farmer.save()
        return farmer


class CustomerManager(BaseUserManager):
    def create_customer(
        self,
        email,
        phone_number,
        first_name,
        last_name,
        location,
        password=None
    ):
        if email is None:
            raise TypeError(
                'Users must have an email address.')  # pragma: no cover
        customer = Customer(
            email=self.normalize_email(email),
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            location=location
            )

        customer.set_password(password)
        customer.save()
        return customer


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_("Phone Number"), max_length=15)
    isFarmer = models.BooleanField(default=False)
    location = models.CharField(
        _("Location"),
        max_length=20,
        default='Lagos'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', ]

    objects = UserManager()

    def __str__(self):
        return self.email


class Farmer(User):
    business_name = models.CharField(_("Business Name"), max_length=50)
    dateTimeCreated = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'business_name', ]

    objects = FarmerManager()

    def __str__(self):
        return self.email


class Customer(User):
    amountOutstanding = models.IntegerField(default=0)
    dateTimeCreated = models.DateField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'phone_number',
        'amountOutstanding',
    ]

    objects = CustomerManager()

    def __str__(self):
        return self.email
