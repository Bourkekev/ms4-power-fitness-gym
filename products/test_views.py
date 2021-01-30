from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

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
        self.staff_user = get_user_model().objects.create_user(
            username='staffuser',
            email='staff@email.com',
            password='secret3',
            is_staff='1',
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

    def test_all_products_view_sort_by_cat(self):
        response = self.client.get('/products/?category=clothing')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/products/?category=clothing"')
        self.assertTemplateUsed(response, 'products/products.html')

    def test_all_products_view_sort_by_sale_price_asc(self):
        response = self.client.get('/products/?sort=sale_price&direction=asc')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_all_products_view_sort_by_name_asc(self):
        response = self.client.get('/products/?sort=name&direction=asc')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_all_products_view_sort_by_name_desc(self):
        response = self.client.get('/products/?sort=name&direction=desc')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_all_products_view_best_sellers(self):
        response = self.client.get('/products/?best_sellers')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Best Seller')
        self.assertTemplateUsed(response, 'products/products.html')

    def test_all_products_view_text_search(self):
        response = self.client.get('/products/?q=test+search')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Products found for')
        self.assertContains(response, 'test search')
        self.assertTemplateUsed(response, 'products/products.html')

    def test_all_products_view_blank_search(self):
        response = self.client.get('/products/?q=')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        expected_message = ('You did not enter any search terms!')
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(str(messages[0]), expected_message)
        self.assertRedirects(response, reverse('products'))

    def test_product_detail_page(self):
        response = self.client.get('/products/1/')
        no_response = self.client.get('/products/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_product_edit_view_logged_in_staff(self):
        self.client.login(
            username='staffuser',
            password='secret3',
        )
        test_product = Product.objects.get(name='Test Product')
        response = self.client.get(reverse(
            'edit_product',
            kwargs={
                'product_id': test_product.id,
            }),
            follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = (f'You are now editing {test_product.name}')
        self.assertEqual(messages[0].tags, 'info')
        self.assertEqual(str(messages[0]), expected_message)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/edit_product.html')

    def test_product_edit_view_not_staff(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        test_product = Product.objects.get(name='Test Product')
        response = self.client.get(reverse(
            'edit_product',
            kwargs={
                'product_id': test_product.id,
            }),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'not authorized to access this page.')

    def test_delete_product_view_logged_in_staff(self):
        self.client.login(
            username='staffuser',
            password='secret3',
        )
        test_product = Product.objects.get(name='Test Product')
        response = self.client.get(reverse(
            'delete_product',
            kwargs={
                'product_id': test_product.id,
            }),
            follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = ('Product deleted!')
        self.assertEqual(messages[0].tags, 'success')
        self.assertEqual(str(messages[0]), expected_message)
        self.assertRedirects(response, '/products/')
        self.assertEqual(response.status_code, 200)

    def test_delete_product_view_not_staff(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        test_product = Product.objects.get(name='Test Product')
        response = self.client.get(reverse(
            'delete_product',
            kwargs={
                'product_id': test_product.id,
            }),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'not authorized to access this page.')
