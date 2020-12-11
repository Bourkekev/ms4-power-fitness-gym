from django.urls import path
from . import views


urlpatterns = [
    path('', views.community_topics, name='community_topics'),
]
