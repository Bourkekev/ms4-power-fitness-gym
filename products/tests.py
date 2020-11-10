from django.test import TestCase
from django.test import SimpleTestCase


# Test Products page loads
class ProductsTests(SimpleTestCase):
    def test_products_page_status_code(self):
        response = self.client.get('products/')
        self.assertEqual(response.status_code, 200)

