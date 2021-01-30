from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .models import Product
from profiles.models import UserProfile
from checkout.models import Order


class TestCheckoutView(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price='10',
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.order = Order.objects.create(
            order_number='testordernumber',
            full_name='Test full name',
            email='test@email.com',
            phone_number='test phone',
            country='IE',
            postcode='test postcode',
            town_or_city='test town',
            street_address1='test address 1',
            street_address2='test address 2',
            county='test county',
            date='2020-11-21 14:26:47.172895',
            delivery_cost='0',
            order_total='57.98',
            grand_total='57.98',
            original_bag='{"1": 3}',
            stripe_pid='pi_00000000000000',
            user_profile=self.user_profile,
        )

    def test_checkout_success(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        test_order = Order.objects.get(id='1')
        response = self.client.get(reverse(
            'checkout_success',
            kwargs={'order_number': test_order}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertContains(response, '57.98')

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
