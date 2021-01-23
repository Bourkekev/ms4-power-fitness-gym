from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestMembershipViews(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

    def test_membership_dashboard_view_logged_in(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        response = self.client.get(reverse('memberships-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'active Membership or subscribe to one.')
        self.assertTemplateUsed(response,
                                'memberships/memberships-dashboard.html')

    def test_subscription_success_get(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        response = self.client.get('/memberships/success/')
        self.assertEqual(response.status_code, 200)

    def test_cancel_subscription_get(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        response = self.client.get('/memberships/cancel/')
        self.assertEqual(response.status_code, 200)
