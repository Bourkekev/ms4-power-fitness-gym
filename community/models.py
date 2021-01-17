from django.db import models
from django.contrib.auth.models import User


class MessageTopic(models.Model):
    """
    * Creates a message topic in database.

    \n Returns __str__:
    * the subject

    \n Other functions return:
    * the number of Messages in a topic
    * the last post
    """
    subject = models.CharField(max_length=255)
    last_update = models.DateTimeField(auto_now_add=True)
    started_by = models.ForeignKey(
        User,
        related_name='topics',
        on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

    def get_posts_count(self):
        return MessagePost.objects.filter(topic__subject=self).count()

    def get_last_post(self):
        return MessagePost.objects.filter(
            topic__subject=self).order_by('-created_at').first()


class MessagePost(models.Model):
    """
    * Creates a message post in database.

    \n Returns __str__:
    * message truncated to 50 characters
    """
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(
        MessageTopic,
        related_name='posts',
        on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User,
        null=True,
        related_name='+',
        on_delete=models.CASCADE)

    def __str__(self):
        return self.message[:50]
