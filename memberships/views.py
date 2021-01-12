from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from memberships.models import StripeSubscription

import stripe


@login_required
def membership_dashboard(request):
    """ membership_dashboard:

    * Displays a user' membership dashboard and shows if \
        they have a subscription

    \n Args:
    1. request: The request

    \n Returns:
    * Subscription, Stripe Product and subscription id to \
        membership dashboard
    """
    try:
        # Retrieve the subscription & product
        stripe_customer = StripeSubscription.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(
            stripe_customer.stripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)
        subscrip_id = subscription.id

        template = 'memberships/memberships-dashboard.html'
        context = {
            'subscription': subscription,
            'product': product,
            'subscrip_id': subscrip_id,
        }
        return render(request, template, context)
    except StripeSubscription.DoesNotExist:
        template = 'memberships/memberships-dashboard.html'
        context = {
            'gold_price_id': settings.STRIPE_GOLD_PRICE_ID,
            'plat_price_id': settings.STRIPE_PLAT_PRICE_ID,
        }
        return render(request, template, context)


@csrf_exempt
def stripe_config(request):
    """ stripe-membership.js fetches stripe public key from here"""
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request, price_id):
    """ create_checkout_session:

    * Creates the checkout session for Stripe subscription

    \n Args:
    1. request
    2. price_id

    \n Returns:
    * JSON Response with session
    """
    if request.method == 'GET':
        stripe_price_id = price_id
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
                        'price': stripe_price_id,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@login_required
def subscription_success(request):
    """Handle if subscription checkout was successful"""
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


@login_required
def upgrade_subscription(request, subscrip_id):
    """ upgrade_subscription:

    * Upgrade a users membership subscription \
      from Gold to Platinum in Stripe

    \n Args:
    1. request: The request
    2. subscrip_id: the ID of the subscription to be upgraded from

    \n Returns:
    * User to membership dahsboard
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # update_from_sub = subscrip_id
    subscription = stripe.Subscription.retrieve(subscrip_id)

    stripe.Subscription.modify(
        subscription.id,
        cancel_at_period_end=False,
        proration_behavior='create_prorations',
        items=[{
            'id': subscription['items']['data'][0].id,
            'price': settings.STRIPE_PLAT_PRICE_ID,
        }]
    )
    return render(request, 'memberships/sub-upgraded.html')


@csrf_exempt
def subscription_webhook(request):
    """ subscription_webhook:

    * Listen for subscription webhooks from Stripe and handles \
        checkout completed event

    \n Args:
    1. request

    \n Returns:
    * HttpResponse to Stripe
    """
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

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new StripeCustomer
        user = User.objects.get(id=client_reference_id)
        StripeSubscription.objects.create(
            user=user,
            stripeCustomerId=stripe_customer_id,
            stripeSubscriptionId=stripe_subscription_id,
        )

    return HttpResponse(status=200)
