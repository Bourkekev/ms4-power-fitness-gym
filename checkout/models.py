import uuid
from django_countries.fields import CountryField

from django.db import models
from django.db.models import Sum
from django.conf import settings

from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    """
    * Creates the order in database. Also contains functions to generate a \
    random order number, update the grand total when a line item is added and \
        override save method to set the order number if it has not been set

    \n Returns __str__:
    * the order number
    """
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
        max_digits=6,
        decimal_places=2,
        null=False, default=0
    )
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False, default=0
    )
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254,
        null=False,
        blank=False,
        default=''
    )
    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True,
                                     related_name='orders')

    def _generate_order_number(self):
        """
        Generates a random, unique order number using UUID

        \n Returns:
        * the unique number
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """ update_total:

        * Update grand total when a line item is added,
        check if order value requires delivery cost and
        adding delivery if needed.

        \n Args:
        1. self: the order

        \n Saves:
        * saves the updated grand_total
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            del_per = settings.STANDARD_DELIVERY_PERCENTAGE
            self.delivery_cost = self.order_total * del_per / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """ save:

        * Override save method to set the order number
        if it has not been set already.

        \n Args:
        1. self: the order
        2. *args:
        3. **kwargs

        \n Save:
        * saves the order with the arguments
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    * Creates the order line items. Also contains function to \
         override the save method to set the line-item total

    \n Returns __str__:
    * the sku on order number
    """
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    product_size = models.CharField(
        max_length=2,
        null=True,
        blank=True
    )
    quantity = models.IntegerField(
        null=False,
        blank=False,
        default=0
    )
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """ save:

    * Override save method to set the line-item total

    \n Args:
    1. self: the order
    2. *args:
    3. **kwargs

    \n Save:
    * saves line-item with args
    """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
