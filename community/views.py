from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import MessageTopic
from .forms import MessageTopicForm


def community_topics(request):
    topics = MessageTopic.objects.all()
    context = {
        'topics': topics,
    }
    return render(request, 'community/community_topics.html', context)


def view_topic(request, topic_id):
    """ A view to show individual topic posts """

    topic = get_object_or_404(MessageTopic, pk=topic_id)
    template = 'community/view_topic.html'
    context = {
        'topic': topic,
    }
    return render(request, template, context)

@login_required
def add_topic(request):
    if request.method == 'POST':
        form = MessageTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.started_by = request.user
            topic.save()
            messages.success(request, 'Topic successfully created')
            return redirect(reverse('community_topics'))
        else:
            messages.error(request,
                           'Failed to add product review. \
                            Please ensure the form is valid.')
    else:
        form = MessageTopicForm()
    template = 'community/add_topic.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
