from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from decimal import Decimal

from .forms import ProductForm
from .models import Product, Review


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

    def test_add_product_view_logged_in_staff(self):
        self.client.login(
            username='staffuser',
            password='secret3',
        )
        response = self.client.post(reverse('add_product'), {
            'name': 'Added Test product',
            'price': '20',
            'description': 'Added product test description'
        })
        self.assertEqual(Product.objects.last().name, 'Added Test product')
        self.assertEqual(Product.objects.last().price, Decimal('20.00'))
        self.assertEqual(
            Product.objects.last().description,
            'Added product test description')
        self.assertEqual(response.status_code, 302)

    def test_edit_product_view_logged_in_staff(self):
        self.client.login(
            username='staffuser',
            password='secret3',
        )
        test_product = Product.objects.get(name='Test Product')
        response = self.client.post(reverse(
            'edit_product',
            kwargs={'product_id': test_product.id}), {
            'name': 'Edited Test product',
            'price': '30',
            'description': 'Edited product test description'
        })
        self.assertEqual(Product.objects.last().name, 'Edited Test product')
        self.assertEqual(Product.objects.last().price, Decimal('30.00'))
        self.assertEqual(
            Product.objects.last().description,
            'Edited product test description')
        self.assertEqual(response.status_code, 302)


class ReviewsTests(TestCase):
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
        self.review = Review.objects.create(
            product=self.product,
            reviewer=self.user,
            review_title='Test review title',
            review='Test review content'
        )
        self.other_user = get_user_model().objects.create_user(
            username='otheruser',
            email='other@email.com',
            password='secret2'
        )

    def test_review_product_login_required(self):
        test_product = Product.objects.get(name='Test Product')
        response = self.client.post(reverse(
            'review_product',
            kwargs={'product_id': test_product.id}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')

    def test_review_product_logged_in(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        test_product = Product.objects.get(name='Test Product')
        response = self.client.post(reverse(
            'review_product',
            kwargs={'product_id': test_product.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add a review')
        self.assertTemplateUsed(response, 'products/add_review.html')

    def test_edit_review_logged_in(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        response = self.client.post(reverse(
            'edit_review',
            kwargs={'review_id': self.review.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit your review')
        self.assertTemplateUsed(response, 'products/edit_review.html')

    def test_edit_review_logged_required(self):
        response = self.client.post(reverse(
            'edit_review',
            kwargs={'review_id': self.review.id}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')

    def test_edit_review_of_other_user(self):
        self.client.login(
            username='otheruser',
            password='secret2',
        )
        response = self.client.post(reverse(
            'edit_review',
            kwargs={'review_id': self.review.id}),
            follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = ('You cannot edit other people\'s reviews!')
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(str(messages[0]), expected_message)
        self.assertRedirects(response, '/profile/')
        self.assertEqual(response.status_code, 200)

    def test_delete_review_login_required(self):
        response = self.client.post(reverse(
            'delete_review',
            kwargs={'review_id': self.review.id}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')

    def test_delete_review_logged_in(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        response = self.client.post(reverse(
            'delete_review',
            kwargs={'review_id': self.review.id}),
            follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = ('Review deleted!')
        self.assertEqual(messages[0].tags, 'success')
        self.assertEqual(str(messages[0]), expected_message)
        self.assertRedirects(response, '/profile/')
        self.assertEqual(response.status_code, 200)

    def test_delete_review_of_other_user(self):
        self.client.login(
            username='otheruser',
            password='secret2',
        )
        response = self.client.post(reverse(
            'delete_review',
            kwargs={'review_id': self.review.id}),
            follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = ('You cannot delete other people\'s reviews!')
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(str(messages[0]), expected_message)
        self.assertRedirects(response, '/profile/')
        self.assertEqual(response.status_code, 200)
