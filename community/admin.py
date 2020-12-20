from django.contrib import admin
from .models import MessageTopic, MessagePost


class MessagePostAdmin(admin.ModelAdmin):
    """
    Create the admin interface for Messages
    """
    readonly_fields = (
        'message',
        'topic',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    list_display = (
        'message',
        'topic',
        'created_at',
        'created_by',
    )

    ordering = ('-created_by',)


admin.site.register(MessageTopic)
admin.site.register(MessagePost, MessagePostAdmin)
