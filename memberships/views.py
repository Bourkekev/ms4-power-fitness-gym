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
    if request.method == 'POST':
        data = json.loads(request.data)
        try:
            # See https://stripe.com/docs/api/checkout/sessions/create
            # for additional parameters to pass.
            # {CHECKOUT_SESSION_ID} is a string literal; do not change it!
            # the actual Session ID is returned in the query parameter when your customer
            # is redirected to the success page.
            checkout_session = stripe.checkout.Session.create(
                success_url="http://127.0.0.1:8000/success.html?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://127.0.0.1:8000/canceled.html",
                payment_method_types=["card"],
                mode="subscription",
                line_items=[
                    {
                        "price": data['priceId'],
                        # For metered billing, do not pass quantity
                        "quantity": 1
                    }
                ],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': {'message': str(e)}}), 400
