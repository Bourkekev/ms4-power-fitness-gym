from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import resolve
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from memberships.models import StripeSubscription

import stripe


@login_required
def membership_dashboard(request):
    print(request.build_absolute_uri())
    try:
        # Retrieve the subscription & product
        stripe_customer = StripeSubscription.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)
        subscrip_id = subscription.id

        return render(request, 'memberships/memberships-dashboard.html', {
            'subscription': subscription,
            'product': product,
            'subscrip_id': subscrip_id,
        })
    except StripeSubscription.DoesNotExist:
        return render(request, 'memberships/memberships-dashboard.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = settings.DOMAIN_URL
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
    """Handle if subscription checkout cancelled before payment"""
    return render(request, 'memberships/cancelled.html')


@login_required
def cancel_subscription(request, subscrip_id):
    """ cancel_subscription:

    * Cancels a users membership subscription \
      in Stripe and delete from database

    \n Args:
    1. request: The request
    2. subscrip_id: the ID of the subscription to be deleted

    \n Renders:
    * Subscription cancelled template
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # delete subscription in stripe
    stripe.Subscription.delete(subscrip_id)

    # Delete subscription in database
    subId = StripeSubscription.objects.get(stripeSubscriptionId=subscrip_id)
    subId.delete()
    return render(request, 'memberships/sub-cancelled.html')


@csrf_exempt
def subscription_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_SUB_WH_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the customer.subscription.created event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # session = event.data.object

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')
        print(client_reference_id)

        # Get the user and create a new StripeCustomer
        user = User.objects.get(id=client_reference_id)
        # print('User :' + user)
        StripeSubscription.objects.create(
            user=user,
            stripeCustomerId=stripe_customer_id,
            stripeSubscriptionId=stripe_subscription_id,
        )
        print(user.username + ' just subscribed.')

    elif event['type'] == 'payment_intent.succeeded':
        print("Payment intent succeeded.")

    else:
        print("WH event not handled")

    return HttpResponse(status=200)
