from django.urls import path
from .views import NewsListView, NewsPostDetailView

urlpatterns = [
    path('<int:pk>/', NewsPostDetailView.as_view(), name='news_post_detail'),
    path('', NewsListView.as_view(), name='news_list'),
]
