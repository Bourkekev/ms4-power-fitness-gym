from django.test import TestCase

from .forms import ProductForm


# Test Products page loads
class ProductFormTests(TestCase):
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

    def test_product_form_minimum_required_fields(self):
        form = ProductForm({
                            'name': 'Test product',
                            'price': '1',
                            'description': 'test description'
                        })
        self.assertTrue(form.is_valid())
