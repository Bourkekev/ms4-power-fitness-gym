from django.urls import path
from .views import HomePageView, GymMemberships
from . import views


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('gym-memberships/', GymMemberships.as_view(), name='gym-memberships'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
]
