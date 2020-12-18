from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    # iterate through each bag item
    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        if product.sale_price:
            price = product.sale_price
        else:
            price = product.price

        # if no size
        if isinstance(item_data, int):
            total += item_data * price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            if 'items_by_shoesize' in item_data.keys():
                for shoesize, quantity in item_data[
                        'items_by_shoesize'].items():
                    total += quantity * price
                    product_count += quantity
                    bag_items.append({
                        'item_id': item_id,
                        'quantity': quantity,
                        'product': product,
                        'shoesize': shoesize,
                    })
            elif 'items_by_clothing_size' in item_data.keys():
                for clothing_size, quantity in item_data[
                        'items_by_clothing_size'].items():
                    total += quantity * price
                    product_count += quantity
                    bag_items.append({
                        'item_id': item_id,
                        'quantity': quantity,
                        'product': product,
                        'clothing_size': clothing_size,
                    })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        left_to_free_delivery = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        left_to_free_delivery = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'left_to_free_delivery': left_to_free_delivery,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
