from django.shortcuts import render, redirect


def view_bag(request):
    """ Return the shopping bag page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add item and quantity to bag """
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    # put bag into session
    request.session['bag'] = bag

    return redirect(redirect_url)