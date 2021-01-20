from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import ProductForm
from .models import Product


# Test Products page loads
class ProductsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price='10',
        )

    def test_string_representation(self):
        product = Product(name='A test product')
        self.assertEqual(str(product), product.name)

    def test_get_product_url(self):
        response = self.client.get('/products/1/')
        self.assertEqual(response.status_code, 200)

    def test_product_content(self):
        self.assertEqual(f'{self.product.name}', 'Test Product')
        self.assertEqual(f'{self.product.description}', 'Test description')
        self.assertEqual(f'{self.product.price}', '10')

    def test_products_page_status_code(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'products/products.html')

    def test_product_detail_page(self):
        response = self.client.get('/products/1/')
        no_response = self.client.get('/products/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_product_edit_view(self):
        response = self.client.post(reverse('edit_product', args='1'), {
            'name': 'Updated Name',
            'description': 'Updated description',
            'price': '16'
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_product_view(self):
        response = self.client.post(
            reverse('delete_product', args='1')
        )
        self.assertEqual(response.status_code, 302)

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

    # def test_get_edit_product_page(self):
    #     response = self.client.get(f'/products/edit/{product.id}')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'products/edit_product.html')
