from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import EditUserProfile
from checkout.models import Order
from products.models import Review


@login_required
def profile(request):
    """
    * Displays the user's profile page

    \n Args:
    1. request

    \n Returns:
    * request, template, context
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    user_reviews = Review.objects.filter(reviewer__username=profile)

    if request.method == 'POST':
        form = EditUserProfile(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
    else:
        form = EditUserProfile(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'profile_name': profile,
        'on_profile_page': True,
        'user_reviews': user_reviews,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    * Shows details of a specific order

    \n Args:
    1. request
    2. order_number

    \n Returns:
    * request, template, context
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}.'
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
