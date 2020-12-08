from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True,
                                 blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2,
                                     null=True, blank=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2,
                                 null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    SHOE_SIZES = (('5', 'Size 5'),
                  ('6', 'Size 6'),
                  ('7', 'Size 7'),
                  ('8', 'Size 8'),
                  ('9', 'Size 9'),
                  ('10', 'Size 10'),
                  ('11', 'Size 11'),
                  ('12', 'Size 12'))

    shoe_sizes = MultiSelectField(choices=SHOE_SIZES, null=True, blank=True)

    CLOTHING_SIZES = (('xs', 'X-Small'),
                      ('s', 'Small'),
                      ('m', 'Medium'),
                      ('l', 'Large'),
                      ('xl', 'X-Large'))

    clothing_sizes = MultiSelectField(choices=CLOTHING_SIZES,
                                      null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    review_title = models.CharField(max_length=50, null=False, blank=False)
    review = models.TextField(max_length=1024, null=False, blank=False)

    def __str__(self):
        return self.review_title
