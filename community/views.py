from django.shortcuts import render, get_object_or_404
from .models import MessageTopic
from .forms import MessageTopicForm


def community_topics(request):
    topics = MessageTopic.objects.all()
    context = {
        'topics': topics,
    }
    return render(request, 'community/community_topics.html', context)


def add_topic(request):
    form = MessageTopicForm()
    template = 'community/add_topic.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
