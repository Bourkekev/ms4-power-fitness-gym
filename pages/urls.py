from django.urls import path
from .views import (
    HomePageView,
    GymMemberships,
    Delivery,
    ReturnPolicy,
    Guarantee,
    SecurePayment,
    CancellationPolicy,
    ImageCredits,
)
from . import views


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('gym-memberships/', GymMemberships.as_view(), name='gym-memberships'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('delivery-information/', Delivery.as_view(), name='delivery'),
    path('return-policy/', ReturnPolicy.as_view(), name='return-policy'),
    path('guarantee/', Guarantee.as_view(), name='guarantee'),
    path('secure-payment/', SecurePayment.as_view(), name='secure-payment'),
    path('cancellation-policy/', CancellationPolicy.as_view(),
         name='cancellation-policy'),
    path('image-credits/', ImageCredits.as_view(), name='image-credits'),
]
