from django.urls import path
from .views import (
    NewsListView,
    NewsPostDetailView,
    NewsPostEditView,
)

urlpatterns = [
    path('<int:pk>/edit/', NewsPostEditView.as_view(), name='news_post_edit'),
    path('<int:pk>/', NewsPostDetailView.as_view(), name='news_post_detail'),
    path('', NewsListView.as_view(), name='news_list'),
]
