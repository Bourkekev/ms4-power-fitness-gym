from django.urls import path
from . import views

urlpatterns = [
    path('', views.membership_dashboard, name='memberships-dashboard'),
]