from django.urls import path
from .views import (
    NewsListView,
    NewsPostDetailView,
    NewsPostEditView,
    NewsPostDeleteView,
    NewsPostCreateView,
)

urlpatterns = [
    path('<int:pk>/edit/', NewsPostEditView.as_view(), name='news_post_edit'),
    path('<int:pk>/delete/',
         NewsPostDeleteView.as_view(), name='news_post_delete'),
    path('<int:pk>/', NewsPostDetailView.as_view(), name='news_post_detail'),
    path('new/', NewsPostCreateView.as_view(), name='news_post_create'),
    path('', NewsListView.as_view(), name='news_list'),
]
