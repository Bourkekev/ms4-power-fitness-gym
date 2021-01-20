from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import UserProfile


class ProfileViewsTests(TestCase):
    # Create test user
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

    def test_profile_view(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')


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
