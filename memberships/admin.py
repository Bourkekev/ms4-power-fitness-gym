from django.contrib import admin
from memberships.models import StripeSubscription

# Register your models here.
admin.site.register(StripeSubscription)
