from django.test import TestCase
from django.urls import reverse


class BagViewsTests(TestCase):
    def test_view_bag_view(self):
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')
