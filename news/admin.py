from django.contrib import admin
from .models import NewsPost


class NewsPostAdmin(admin.ModelAdmin):
    """ Creates the admin interface for News Posts """
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ("status",)
    search_fields = ['title', 'body']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(NewsPost, NewsPostAdmin)
