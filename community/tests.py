from django.urls import reverse
from django.test import TestCase


class MessageBoardTests(TestCase):
    def test_community_topics_view_status_code(self):
        url = reverse('community_topics')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
