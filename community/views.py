from django.shortcuts import render
from .models import MessageTopic


def community_topics(request):
    topics = MessageTopic.objects.all()
    context = {
        'topics': topics,
    }
    return render(request, 'community/community_topics.html', context)
