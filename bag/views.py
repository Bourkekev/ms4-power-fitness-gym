from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Product


def view_bag(request):
    """ Return the shopping bag page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ add_to_bag:

    * Adds an item's quantity and size to the bag

    \n Args:
    1. request: the POST request data from the form
    2. item_id: the ID of the item to be added

    \n Redirects:
    * User back to same page (or reloads current page)
    """
    product = Product.objects.get(pk=item_id)  # needed for toast
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    shoesize = None
    if 'shoe_size' in request.POST:
        shoesize = request.POST['shoe_size']

    clothing_size = None
    if 'clothing_size' in request.POST:
        clothing_size = request.POST['clothing_size']

    bag = request.session.get('bag', {})

    if shoesize or clothing_size:
        if shoesize:
            if item_id in list(bag.keys()):
                if shoesize in bag[item_id]['items_by_shoesize'].keys():
                    bag[item_id]['items_by_shoesize'][shoesize] += quantity
                else:
                    bag[item_id]['items_by_shoesize'][shoesize] = quantity
            else:
                bag[item_id] = {'items_by_shoesize': {shoesize: quantity}}
        elif clothing_size:
            if item_id in list(bag.keys()):
                if (clothing_size in
                        bag[item_id]['items_by_clothing_size'].keys()):
                    bag[item_id][
                        'items_by_clothing_size'][clothing_size] += quantity
                else:
                    bag[item_id][
                        'items_by_clothing_size'][clothing_size] = quantity
            else:
                bag[item_id] = {
                    'items_by_clothing_size': {clothing_size: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Added {product.name} to your shopping bag')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your shopping bag')

    # put bag into session
    request.session['bag'] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ adjust_bag:

    * Adjusts an item's quantity in the bag

    \n Args:
    1. request: the POST request data from the form
    2. item_id: the ID of the item to be adjusted

    \n Redirects:
    * User back to bag page (or reloads bag page)
    """
    quantity = int(request.POST.get('quantity'))
    shoesize = None
    if 'shoe_size' in request.POST:
        shoesize = request.POST['shoe_size']

    clothing_size = None
    if 'clothing_size' in request.POST:
        clothing_size = request.POST['clothing_size']

    bag = request.session.get('bag', {})

    if shoesize or clothing_size:
        if shoesize:
            if quantity > 0:
                bag[item_id]['items_by_shoesize'][shoesize] = quantity
            else:
                del bag[item_id]['items_by_shoesize'][shoesize]
                if not bag[item_id]['items_by_shoesize']:
                    bag.pop(item_id)
        elif clothing_size:
            if quantity > 0:
                bag[item_id][
                    'items_by_clothing_size'][clothing_size] = quantity
            else:
                del bag[item_id][
                        'items_by_clothing_size'][clothing_size]
                if not bag[item_id]['items_by_clothing_size']:
                    bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    # put bag into session
    request.session['bag'] = bag

    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ remove_from_bag:

    * Removes the item from the bag

    \n Args:
    1. request: the POST request data from the form
    2. item_id: the ID of the item to be removed

    \n Returns:
    * 200 http response
    """
    try:
        shoesize = None
        if 'shoe_size' in request.POST:
            shoesize = request.POST['shoe_size']

        clothing_size = None
        if 'clothing_size' in request.POST:
            clothing_size = request.POST['clothing_size']

        bag = request.session.get('bag', {})
        if shoesize or clothing_size:
            if shoesize:
                del bag[item_id]['items_by_shoesize'][shoesize]
                if not bag[item_id]['items_by_shoesize']:
                    bag.pop(item_id)
            elif clothing_size:
                del bag[item_id][
                        'items_by_clothing_size'][clothing_size]
                if not bag[item_id]['items_by_clothing_size']:
                    bag.pop(item_id)
        else:
            bag.pop(item_id)

        # put bag into session
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
