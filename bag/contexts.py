from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    
    # for item in bag:
    #     print(bag[item])
    #     if 'items_by_shoesize' in bag[item]:
    #         print('Has shoe size')
    print(bag.items())
    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            print('Value is int')
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            print('Value is dict')
            # print(item_data['items_by_shoesize'])
            if 'items_by_shoesize' in item_data.keys():
                print("Shoesize Present, ", end =" ") 
                print("value =", item_data['items_by_shoesize'])
                product = get_object_or_404(Product, pk=item_id)
                for shoesize, quantity in item_data['items_by_shoesize'].items():
                    total += quantity * product.price
                    product_count += quantity
                    bag_items.append({
                        'item_id': item_id,
                        'quantity': quantity,
                        'product': product,
                        'shoesize': shoesize,
                    })
            elif 'items_by_clothing_size' in item_data.keys():
                print("Clothes size Present, ", end =" ") 
                print("value =", item_data['items_by_clothing_size'])
                product = get_object_or_404(Product, pk=item_id)
                for clothing_size, quantity in item_data['items_by_clothing_size'].items():
                    total += quantity * product.price
                    product_count += quantity
                    bag_items.append({
                        'item_id': item_id,
                        'quantity': quantity,
                        'product': product,
                        'clothing_size': clothing_size,
                    })
            else: 
                print("Not present")
        

    
    # loop through items in bag
    # for item_id, item_data in bag.items():

        # if int then is only qty
        # if isinstance(item_data, int):
        #     product = get_object_or_404(Product, pk=item_id)
        #     total += item_data * product.price
        #     product_count += item_data
        #     bag_items.append({
        #         'item_id': item_id,
        #         'quantity': item_data,
        #         'product': product,
        #     })
        # else:
        #     product = get_object_or_404(Product, pk=item_id)
        #     for shoesize, quantity in item_data['items_by_shoesize'].items():
        #         total += quantity * product.price
        #         product_count += quantity
        #         bag_items.append({
        #             'item_id': item_id,
        #             'quantity': quantity,
        #             'product': product,
        #             'shoesize': shoesize,
        #         })


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
