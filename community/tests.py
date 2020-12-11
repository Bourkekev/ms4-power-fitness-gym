from django.urls import reverse, resolve
from django.test import TestCase
from .views import community_topics


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
