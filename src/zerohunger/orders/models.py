from django.db import models
from accounts.models import User
from product.models import Produce

# Create your models here.


class Orders(models.Model):
    CHOICES = (
        ('P', 'Proccesing'),
        ('T', 'In-Transit'),
        ('C', 'Canceled'),
        ('D', 'Delivered')
    )
    customer_id = models.ForeignKey(
        User, related_name='customers', on_delete=models.CASCADE)
    amount_paid = models.FloatField(blank=True, null=True)
    order_status = models.CharField(max_length=1, choices=CHOICES, default='P')
    dateAndTimeOfOrder = models.DateTimeField(auto_now_add=True)
    amount_due = models.FloatField(blank=True, null=True)
    has_paid = models.BooleanField(default=False)
    items_ordered = models.ManyToManyField(
        Produce, through='ItemsOrdered')
    create_date = models.DateTimeField(auto_now_add=True)

    @property
    def amount_outstanding(self):
        return float(self.amount_due - self.amount_paid)


class ItemsOrdered(models.Model):
    produce = models.ForeignKey(Produce, related_name='produce',
                                on_delete=models.CASCADE)
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    dateTimeCreated = models.DateField(auto_now_add=True)
