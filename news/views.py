from django.views.generic import ListView, DetailView
from .models import NewsPost


class NewsListView(ListView):
    model = NewsPost
    template_name = 'news/news_list.html'


class NewsPostDetailView(DetailView):
    model = NewsPost
    template_name = 'news/news_post_detail.html'
