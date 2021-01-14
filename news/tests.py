from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import NewsPost


class NewsPostModelTest(TestCase):
    # Create test post
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        self.post = NewsPost.objects.create(
            title='A test title',
            body='Test body text',
            author=self.user,
        )

    def test_string_representation(self):
        post = NewsPost(title='A test title')
        self.assertEqual(str(post), post.title)

    # Test for setUp NewsPost content
    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A test title')
        self.assertEqual(f'{self.post.body}', 'Test body text')
        self.assertEqual(f'{self.post.author}', 'testuser')

    def test_post_list_view(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
