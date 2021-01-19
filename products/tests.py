from django.test import TestCase

from .forms import ProductForm


# Test Products page loads
class ProductsTests(TestCase):
    def test_products_page_status_code(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_add_product_form_required_fields(self):
        form = ProductForm({'name': ''})
        form = ProductForm({'description': ''})
        form = ProductForm({'price': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertEqual(form.errors['name'][0], 'This field is required.')
        self.assertIn('description', form.errors.keys())
        self.assertEqual(
            form.errors['description'][0], 'This field is required.'
        )
        self.assertIn('price', form.errors.keys())
        self.assertEqual(form.errors['price'][0], 'This field is required.')
