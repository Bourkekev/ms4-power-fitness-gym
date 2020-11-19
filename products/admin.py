from django.contrib import admin
from .models import Product, Category


class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'price',
        'category',
        'image',
    )

    ordering = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Product, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)