import uuid
from decimal import Decimal, ROUND_UP

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField

from products.models import Wine
from profiles.models import UserProfile


class Order(models.Model):

    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Paid & Processing'),
        ('shipped', 'Shipped'),
        ('fulfilled', 'Fulfilled'),
        ('returned', 'Returned & Refunded'),
    ]
    # Relationships
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders')

    # Fields
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=Decimal('0.00'))
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=Decimal('0.00'))
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=Decimal('0.00'))
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return f"ORD-{uuid.uuid4().hex[:8].upper()}"

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or Decimal('0.00')

        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total * Decimal(
                    settings.STANDARD_DELIVERY_PERCENTAGE) / (
                    Decimal('100'))).quantize(Decimal('0.01'))
        else:
            self.delivery_cost = Decimal('0.00')

        self.grand_total = (
            self.order_total + self.delivery_cost).quantize(Decimal('0.01'))
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    # Relationship
    order = models.ForeignKey(
        Order, null=False, blank=False,
        on_delete=models.CASCADE, related_name='lineitems')
    wine = models.ForeignKey(
        Wine, null=False, blank=False, on_delete=models.CASCADE)
    # Fields
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False,
        blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        price = Decimal(self.wine.price)  # Ensure price is a Decimal
        quantity = Decimal(self.quantity)  # Ensure quantity is a Decimal
        self.lineitem_total = (price * quantity).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
