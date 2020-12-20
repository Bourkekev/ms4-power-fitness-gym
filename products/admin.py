from django.contrib import admin
from .models import Product, Category, Review


class ReviewInline(admin.TabularInline):
    model = Review


class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'price',
        'category',
        'image',
    )

    ordering = ('name',)

    inlines = [
        ReviewInline,
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'review_title',
        'reviewer',
        'product',
    )


admin.site.register(Product, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
