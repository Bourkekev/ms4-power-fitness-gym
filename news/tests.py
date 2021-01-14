from django.contrib.auth import get_user_model
from django.test import TestCase
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

    # Test for setUp NewsPost title
    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A test title')
        self.assertEqual(f'{self.post.body}', 'Test body text')
