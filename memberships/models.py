from django.contrib.auth.models import User
from django.db import models


class StripeSubscription(models.Model):
    """
    * Creates a Stripe Subscription in database.

    \n Returns __str__:
    * Username
    """
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
