from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .models import Product


class TestCheckoutView(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price='10',
        )

    def test_checkout_view(self):
        test_product = Product.objects.get(name='Test Product')
        session = self.client.session
        session['bag'] = {test_product.id: 1}
        session.save()
        response = self.client.get(reverse('checkout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_empty_basket_on_checkout(self):
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, '/products/')
        messages = list(get_messages(response.wsgi_request))
        expected_message = "There's nothing in your bag at the moment."
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(str(messages[0]), expected_message)
