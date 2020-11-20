from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'checkout'

    def ready(self):
        """
        Update order totals when line item changed/deleted
        """
        import checkout.signals
