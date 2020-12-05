from django.contrib import admin

from .models import ContactForm


class ContactFormAdmin(admin.ModelAdmin):
    """
    Create the admin interface for Contact Forms
    """
    readonly_fields = (
        'subject',
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'your_message',
        'date_sent',
    )

    list_display = (
        'subject',
        'answered',
        'first_name',
        'email',
        'date_sent',
    )

    ordering = ('-date_sent',)


admin.site.register(ContactForm, ContactFormAdmin)
