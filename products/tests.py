from django.test import TestCase


# Test Products page loads
class ProductsTests(TestCase):
    def test_products_page_status_code(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
