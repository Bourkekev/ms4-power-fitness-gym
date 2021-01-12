from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    UpdateView, DeleteView, CreateView
)
from django.urls import reverse_lazy
from .models import NewsPost


class NewsListView(ListView):
    """
    * Creates a page with a list view of News Posts

    \n Attributes:
    1. queryset: the set of database objects
    2. The Model
    3. template_name: template to be used
    4. paginate_by: number of items to show before pagination

    """
    queryset = NewsPost.objects.filter(status=1)
    model = NewsPost
    template_name = 'news/news_list.html'
    paginate_by = 3


class NewsPostDetailView(DetailView):
    """
    * Creates a page for the detail of the News Post

    \n Attributes:
    1. The Model
    2. template_name: template to be used

    """
    model = NewsPost
    template_name = 'news/news_post_detail.html'


class NewsPostEditView(PermissionRequiredMixin, UpdateView):
    """
    * Creates a page for editing a News Post and sets the \
        permission required for this.

    \n Attributes:
    1. permission_required: user permission
    2. The Model
    3. fields: the fields to show from the model
    4. template_name: template to be used

    """
    permission_required = 'user.is_staff'
    permission_denied_message = 'Your access level does \
        not allow you to edit a news item!'
    model = NewsPost
    fields = ('title', 'body', 'status')
    template_name = 'news/news_post_edit.html'


class NewsPostDeleteView(PermissionRequiredMixin, DeleteView):
    """
    * Deletes a News Post and sets the \
        permission required for this.

    \n Attributes:
    1. permission_required: user permission
    2. The Model
    3. success_url: Where to send the user after deletion

    """
    permission_required = 'user.is_staff'
    permission_denied_message = 'Your access level does \
        not allow you to delete a news item!'
    model = NewsPost
    success_url = reverse_lazy('news_list')


class NewsPostCreateView(PermissionRequiredMixin, CreateView):
    """
    * Creates a new News Post and sets the \
        permission required for this.

    \n Attributes:
    1. permission_required: user permission
    2. The Model
    3. fields: the fields to show from the model
    4. template_name: template to be used

    """
    permission_required = 'user.is_staff'
    permission_denied_message = 'Your access level does \
        not allow you to add a news item!'
    model = NewsPost
    fields = ('title', 'body', 'status')
    template_name = 'news/news_post_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
