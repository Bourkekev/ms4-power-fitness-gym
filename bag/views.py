from django.shortcuts import render, redirect


def view_bag(request):
    """ Return the shopping bag page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add item and quantity to bag """
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
                if clothing_size in bag[item_id]['items_by_clothing_size'].keys():
                    bag[item_id]['items_by_clothing_size'][clothing_size] += quantity
                else:
                    bag[item_id]['items_by_clothing_size'][clothing_size] = quantity
            else:
                bag[item_id] = {'items_by_clothing_size': {clothing_size: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    # put bag into session
    request.session['bag'] = bag

    return redirect(redirect_url)
