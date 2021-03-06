from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.test import TestCase

from .views import community_topics, view_topic
from .models import MessagePost, MessageTopic


class MessageBoardTests(TestCase):
    def test_community_topics_view_status_code(self):
        url = reverse('community_topics')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_community_url_resolves_community_topics_view(self):
        view = resolve('/community/')
        self.assertEquals(view.func, community_topics)

    def test_community_topics_view_contains_add_topic_button(self):
        """ Test that the Community Topics page contains an add_topic link"""
        community_topics_url = reverse('community_topics')
        add_topic_url = reverse('add_topic')
        response = self.client.get(community_topics_url)
        self.assertContains(response, 'href="{0}"'.format(add_topic_url))


class ViewTopicTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )
        self.topic = MessageTopic.objects.create(
            subject='Test Create Topic',
            started_by=self.user,
        )
        self.post = MessagePost.objects.create(
            message='Lorem ipsum dolor sit amet',
            topic=self.topic,
            created_by=self.user,
        )
        self.other_user = get_user_model().objects.create_user(
            username='otheruser',
            email='other@email.com',
            password='secret2'
        )

    def test_view_function(self):
        view = resolve('/community/topic/1/')
        self.assertEquals(view.func, view_topic)

    # Test for setUp MessagePost content
    def test_post_content(self):
        self.assertEqual(f'{self.post.topic}', 'Test Create Topic')
        self.assertEqual(f'{self.post.message}', 'Lorem ipsum dolor sit amet')
        self.assertEqual(f'{self.post.created_by}', 'testuser')

    def test_message_board_view(self):
        response = self.client.get(reverse('community_topics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Create Topic')
        self.assertTemplateUsed(response, 'community/community_topics.html')

    def test_view_topic_view_logged_in(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        test_topic = MessageTopic.objects.get(subject='Test Create Topic')
        response = self.client.get(reverse(
            'view_topic',
            kwargs={'topic_id': test_topic.id},
            ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Create Topic')
        self.assertTemplateUsed(response, 'community/view_topic.html')

    def test_view_topic_view_not_logged_in(self):
        test_topic = MessageTopic.objects.get(subject='Test Create Topic')
        response = self.client.get(reverse(
            'view_topic',
            kwargs={'topic_id': test_topic.id},
            ),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')

    def test_add_topic_get_page_not_logged_in(self):
        response = self.client.get(reverse(
            'add_topic'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')

    def test_add_topic_get_page_logged_in(self):
        self.client.login(
            username='otheruser',
            password='secret2',
        )
        response = self.client.get(reverse(
            'add_topic'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add a new Topic')
        self.assertTemplateUsed(response, 'community/add_topic.html')
