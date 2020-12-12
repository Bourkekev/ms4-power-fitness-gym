
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase, Client

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
        user = User.objects.create_user(
            username='john',
            email='john@doe.com',
            password='123')
        topic = MessageTopic.objects.create(
            subject='Hello, world',
            started_by=user)
        MessagePost.objects.create(
            message='Lorem ipsum dolor sit amet',
            topic=topic,
            created_by=user)
        url = reverse('view_topic', kwargs={'topic_id': topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        c = Client()
        c.login(username='john', password='123')
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/community/topic/1/')
        self.assertEquals(view.func, view_topic)
