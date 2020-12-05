from django.urls import path
from .views import HomePageView, GymMemberships
from . import views


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('gym-memberships/', GymMemberships.as_view(), name='gym-memberships'),
    # path('contact/', ContactPage.as_view(), name='contact'),
    path('contact/', views.contact,
         name='contact'),
]
