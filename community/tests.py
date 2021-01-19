
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
            username='john',
            email='john@doe.com',
            password='123',
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

    def test_view_function(self):
        view = resolve('/community/topic/1/')
        self.assertEquals(view.func, view_topic)

    # Test for setUp MessagePost content
    def test_post_content(self):
        self.assertEqual(f'{self.post.topic}', 'Test Create Topic')
        self.assertEqual(f'{self.post.message}', 'Lorem ipsum dolor sit amet')
        self.assertEqual(f'{self.post.created_by}', 'john')

    def test_message_board_view(self):
        response = self.client.get(reverse('community_topics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Create Topic')
        self.assertTemplateUsed(response, 'community/community_topics.html')
