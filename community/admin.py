from django.contrib import admin
from .models import MessageTopic, MessagePost


admin.site.register(MessageTopic)
admin.site.register(MessagePost)
