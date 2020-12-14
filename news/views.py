from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import NewsPost


class NewsListView(ListView):
    model = NewsPost
    template_name = 'news/news_list.html'


class NewsPostDetailView(DetailView):
    model = NewsPost
    template_name = 'news/news_post_detail.html'


class NewsPostEditView(UpdateView):
    model = NewsPost
    fields = ('title', 'body',)
    template_name = 'news/news_post_edit.html'


class NewsPostDeleteView(DeleteView):
    model = NewsPost
    template_name = 'news/news_post_delete.html'
    success_url = reverse_lazy('news_list')
