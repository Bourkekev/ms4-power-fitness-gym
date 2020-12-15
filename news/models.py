from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

STATUS = (
    (0, 'Draft'),
    (1, 'Published')
)


class NewsPost(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_post_detail', args=[str(self.id)])
