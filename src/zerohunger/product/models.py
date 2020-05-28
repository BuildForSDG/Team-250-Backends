from django.db import models
from accounts.models import User
from cloudinary.models import CloudinaryField
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Produce(models.Model):
    name = models.CharField(_("Name"), max_length=100,
                            help_text="Name of the product")
    price = models.FloatField(
        _("Price per Bag"), help_text="Price of the Product (Float)")
    farmer_id = models.ForeignKey(
        User, verbose_name=_("Farmer"),
        on_delete=models.CASCADE,
        related_name='farmer_produce',
        help_text="Farmer Id, gotten from request.user"
    )
    description = models.TextField(
        _("Description of the product"),
        help_text="Product Description (Text Field)")
    quantity = models.IntegerField(
        _("Quantity Available"),
        help_text="Quantity of Product Available")
    product_img = CloudinaryField('product_image')
    create_date = models.DateTimeField(
        _("Date of Creation"), auto_now_add=True)

    def __str__(self):
        return self.name
