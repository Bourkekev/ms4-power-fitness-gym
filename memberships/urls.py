from django.urls import path
from . import views

urlpatterns = [
    path('', views.membership_dashboard, name='memberships-dashboard'),
    path('config/', views.stripe_config),
    path('create-checkout-session/<price_id>', views.create_checkout_session),
    path('success/', views.subscription_success),
    path('cancel/', views.subscription_cancel),
    path('subwh/', views.subscription_webhook),
    path('cancel-subscription/<subscrip_id>', views.cancel_subscription, name='cancel-subscription'),
]
