# Generated by Django 3.1.3 on 2021-01-19 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_is_best_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
    ]