from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    UpdateView, DeleteView, CreateView
)
from django.urls import reverse_lazy
from .models import NewsPost


class NewsListView(ListView):
    model = NewsPost
    template_name = 'news/news_list.html'


class NewsPostDetailView(DetailView):
    model = NewsPost
    template_name = 'news/news_post_detail.html'


class NewsPostEditView(PermissionRequiredMixin, UpdateView):
    permission_required = 'user.is_staff'
    permission_denied_message = 'Your access level does \
        not allow you to edit a news item!'
    model = NewsPost
    fields = ('title', 'body',)
    template_name = 'news/news_post_edit.html'


class NewsPostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'user.is_staff'
    permission_denied_message = 'Your access level does \
        not allow you to delete a news item!'
    model = NewsPost
    success_url = reverse_lazy('news_list')


class NewsPostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'user.is_staff'
    permission_denied_message = 'Your access level does \
        not allow you to add a news item!'
    model = NewsPost
    fields = ('title', 'body',)
    template_name = 'news/news_post_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
