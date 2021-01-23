from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from products.models import Product


class BagViewsTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price='10',
            shoe_sizes='7',
            clothing_sizes='m',
        )

    def test_view_bag_view(self):
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_add_to_bag_view(self):
        test_product = Product.objects.get(name='Test Product')
        response = self.client.post(reverse(
            'add_to_bag',
            kwargs={'item_id': test_product.id}),
            data={
                'quantity': '1',
                'redirect_url': '/',
            }
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = (f'Added {test_product.name} to your shopping bag')
        self.assertEqual(messages[0].tags, 'Add to shopping bag success')
        self.assertEqual(str(messages[0]), expected_message)

    def test_add_to_bag_with_shoesize_view(self):
        test_product = Product.objects.get(name='Test Product')
        posted_data = {
            'quantity': '1',
            'redirect_url': '/',
            'shoe_size': '7'
        }
        response = self.client.post(reverse(
            'add_to_bag',
            kwargs={'item_id': test_product.id}),
            data=posted_data,
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = (f"Added size {posted_data['shoe_size'].upper()} "
                            f"{test_product.name} to your bag")
        self.assertEqual(messages[0].tags, 'success')
        self.assertEqual(str(messages[0]), expected_message)

    def test_add_to_bag_with_shoesize_another_item_view(self):
        test_product = Product.objects.get(name='Test Product')
        posted_data = {
            'quantity': '1',
            'redirect_url': '/',
            'shoe_size': '7'
        }
        response = self.client.post(reverse(
            'add_to_bag',
            kwargs={'item_id': test_product.id}),
            data=posted_data,
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = (f"Added size {posted_data['shoe_size'].upper()} "
                            f"{test_product.name} to your bag")
        self.assertEqual(messages[0].tags, 'success')
        self.assertEqual(str(messages[0]), expected_message)

        # Test add another of same item
        another_response = self.client.post(reverse(
            'add_to_bag',
            kwargs={'item_id': test_product.id}),
            data=posted_data,
        )
        messages = list(get_messages(another_response.wsgi_request))
        expected_message = (f"Updated size {posted_data['shoe_size'].upper()} "
                            f"{test_product.name} quantity to "
                            f"2")
        self.assertEqual(messages[1].tags, 'Shopping bag updated success')
        self.assertEqual(str(messages[1]), expected_message)

    def test_add_to_bag_with_clothing_size_view(self):
        test_product = Product.objects.get(name='Test Product')
        posted_data = {
            'quantity': '1',
            'redirect_url': '/',
            'clothing_size': 'm'
        }
        response = self.client.post(reverse(
            'add_to_bag',
            kwargs={'item_id': test_product.id}),
            data=posted_data,
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = (f"Added size {posted_data['clothing_size'].upper()} "
                            f"{test_product.name} to your bag")
        self.assertEqual(messages[0].tags, 'Shopping bag updated success')
        self.assertEqual(str(messages[0]), expected_message)

    def test_add_to_bag_with_clothing_size_another_item_view(self):
        test_product = Product.objects.get(name='Test Product')
        posted_data = {
            'quantity': '1',
            'redirect_url': '/',
            'clothing_size': 'm'
        }
        response = self.client.post(reverse(
            'add_to_bag',
            kwargs={'item_id': test_product.id}),
            data=posted_data,
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = (f"Added size {posted_data['clothing_size'].upper()} "
                            f"{test_product.name} to your bag")
        self.assertEqual(messages[0].tags, 'Shopping bag updated success')
        self.assertEqual(str(messages[0]), expected_message)

        # Test add another of same item
        another_response = self.client.post(reverse(
            'add_to_bag',
            kwargs={'item_id': test_product.id}),
            data=posted_data,
        )
        messages = list(get_messages(another_response.wsgi_request))
        expected_message = (f"Updated size {posted_data['clothing_size'].upper()} "
                            f"{test_product.name} quantity to "
                            f"2")
        self.assertEqual(messages[1].tags, 'Shopping bag updated success')
        self.assertEqual(str(messages[1]), expected_message)

    def test_adjust_bag_view(self):
        # First add test product to bag
        test_product = Product.objects.get(name='Test Product')
        self.client.post(reverse(
            'add_to_bag',
            kwargs={'item_id': test_product.id}),
            data={
                'quantity': '1',
                'redirect_url': '/',
            }
        )
        # Test update item quantity in bag
        response = self.client.post(reverse(
            'adjust_bag',
            kwargs={'item_id': test_product.id}),
            data={
                'quantity': '3',
                'redirect_url': '/',
            }
        )
        update_messages = list(get_messages(response.wsgi_request))
        expected_message = (f'Updated {test_product.name} quantity '
                            f'to 3')
        self.assertEqual(update_messages[1].tags,
                         'Shopping bag updated success')
        self.assertEqual(str(update_messages[1]), expected_message)

    def test_adjust_bag_with_shoesize_quantity_view(self):
        test_product = Product.objects.get(name='Test Product')
        posted_data = {
            'quantity': '1',
            'redirect_url': '/',
            'shoe_size': '7'
        }
        response = self.client.post(reverse(
            'add_to_bag',
            kwargs={'item_id': test_product.id}),
            data=posted_data,
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = (f"Added size {posted_data['shoe_size'].upper()} "
                            f"{test_product.name} to your bag")
        self.assertEqual(messages[0].tags, 'success')
        self.assertEqual(str(messages[0]), expected_message)

        # Test adjust quantity same item
        qty_updated_data = {
            'quantity': '3',
            'redirect_url': '/',
            'shoe_size': '7'
        }
        another_response = self.client.post(reverse(
            'adjust_bag',
            kwargs={'item_id': test_product.id}),
            data=qty_updated_data,
        )
        messages = list(get_messages(another_response.wsgi_request))
        expected_message = (f"Updated size {qty_updated_data['shoe_size'].upper()} "
                            f"{test_product.name} quantity to "
                            f"{qty_updated_data['quantity']}")
        self.assertEqual(messages[1].tags, 'Shopping bag updated success')
        self.assertEqual(str(messages[1]), expected_message)

    def test_adjust_bag_with_clothing_size_quantity_view(self):
        test_product = Product.objects.get(name='Test Product')
        posted_data = {
            'quantity': '1',
            'redirect_url': '/',
            'clothing_size': 'm'
        }
        response = self.client.post(reverse(
            'add_to_bag',
            kwargs={'item_id': test_product.id}),
            data=posted_data,
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = (f"Added size {posted_data['clothing_size'].upper()} "
                            f"{test_product.name} to your bag")
        self.assertEqual(messages[0].tags, 'Shopping bag updated success')
        self.assertEqual(str(messages[0]), expected_message)

        # Test adjust quantity same item
        qty_updated_data = {
            'quantity': '3',
            'redirect_url': '/',
            'clothing_size': 'm'
        }
        another_response = self.client.post(reverse(
            'adjust_bag',
            kwargs={'item_id': test_product.id}),
            data=qty_updated_data,
        )
        messages = list(get_messages(another_response.wsgi_request))
        expected_message = (f"Updated size {qty_updated_data['clothing_size'].upper()} "
                            f"{test_product.name} quantity to "
                            f"{qty_updated_data['quantity']}")
        self.assertEqual(messages[1].tags, 'Shopping bag updated success')
        self.assertEqual(str(messages[1]), expected_message)

    def test_remove_from_bag(self):
        # First add test product to bag
        test_product = Product.objects.get(name='Test Product')
        self.client.post(reverse(
            'add_to_bag',
            kwargs={'item_id': test_product.id}),
            data={
                'quantity': '1',
                'redirect_url': '/',
            }
        )
        # Test remove item from bag
        response = self.client.post(reverse(
            'remove_from_bag',
            kwargs={'item_id': test_product.id})
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = (f'Removed {test_product.name} from your bag')
        self.assertEqual(messages[1].tags,
                         'Shopping bag updated success')
        self.assertEqual(str(messages[1]), expected_message)
