from django.contrib import admin

from .models import ContactForm


class ContactFormAdmin(admin.ModelAdmin):
    """
    Create the admin interface for Contact Forms
    """
    list_display = (
        'subject',
        'first_name',
        'email',
    )


admin.site.register(ContactForm, ContactFormAdmin)
