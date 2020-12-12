from django.urls import path
from . import views


urlpatterns = [
    path('', views.community_topics, name='community_topics'),
    path('topic/<int:topic_id>/', views.view_topic, name='view_topic'),
    path('topic/<int:topic_id>/reply/', views.reply_topic, name='reply_topic'),
    path('add_topic', views.add_topic, name='add_topic'),
]
