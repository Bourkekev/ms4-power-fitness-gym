from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .forms import EditUserProfile
from .models import UserProfile
from checkout.models import Order


class ProfileViewsTests(TestCase):
    # Create test user
    def setUp(self):
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

    def test_profile_view(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_profile_post_update(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        response = self.client.post(reverse('profile'), {
            'default_phone_number': 'Test phone',
            'default_street_address1': 'Test address 1',
            'default_street_address2': 'Test address 2',
            'default_town_or_city': 'Test town',
            'default_county': 'Test county',
            'default_postcode': 'Test postcode',
            'default_country': 'IE',
        },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        messages = list(get_messages(response.wsgi_request))
        expected_message = ('Profile updated successfully')
        self.assertEqual(messages[0].tags, 'success')
        self.assertEqual(str(messages[0]), expected_message)

    def test_order_history(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        test_order = Order.objects.get(id='1')
        response = self.client.get(reverse(
            'order_history',
            kwargs={'order_number': test_order}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertContains(response, 'Completed Order Details')
        self.assertContains(response, '57.98')


class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

    def test_user_profile_string_representation(self):
        test_user = UserProfile.objects.get(user__username='testuser')
        self.assertEqual(str(test_user), 'testuser')

    def test_edit_user_profile_form(self):
        test_user = UserProfile.objects.get(user__username='testuser')
        form = EditUserProfile({
                            'user': test_user,
                            'default_phone_number': 'Test phone',
                            'default_street_address1': 'test address1',
                            'default_street_address2': 'test address2',
                            'default_town_or_city': 'test town',
                            'default_county': 'test county',
                            'default_postcode': 'Test post code',
                            'default_country': 'IE',
                        })
        self.assertTrue(form.is_valid())
