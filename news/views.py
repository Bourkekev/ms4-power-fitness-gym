from django.views.generic import ListView
from .models import NewsPost


class NewsListView(ListView):
    model = NewsPost
    template_name = 'news/news_list.html'
