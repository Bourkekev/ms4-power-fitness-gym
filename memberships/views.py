from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import stripe


@login_required
def membership_dashboard(request):
    return render(request, 'memberships/memberships-dashboard.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'memberships/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'memberships/cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_GOLD_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@login_required
def subscription_success(request):
    return render(request, 'memberships/successful.html')


@login_required
def subscription_cancel(request):
    return render(request, 'memberships/cancelled.html')
