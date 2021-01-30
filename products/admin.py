from django.conf import settings
from django.contrib import admin
from .models import Product, Category, Review


class ReviewInline(admin.TabularInline):
    """ Allows view/edit of reviews from Product detail page """
    model = Review


class ProductsAdmin(admin.ModelAdmin):
    """ Creates the admin interface for Products """
    list_display = (
        'name',
        'sku',
        'price',
        'category',
        'image',
    )

    ordering = ('name',)

    inlines = [
        ReviewInline,
    ]

    class Media:
        js = (settings.STATIC_URL + 'admin/js/assets_admin.js',)


class CategoryAdmin(admin.ModelAdmin):
    """ Creates the admin interface for Product Categories """
    list_display = (
        'friendly_name',
        'name',
    )


class ReviewAdmin(admin.ModelAdmin):
    """ Creates the admin interface for Product Reviews """
    list_display = (
        'review_title',
        'reviewer',
        'product',
    )


admin.site.register(Product, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
