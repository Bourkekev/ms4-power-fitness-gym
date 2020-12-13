from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import MessageTopic, MessagePost
from .forms import MessageTopicForm, MessagePostForm


def community_topics(request):
    topics = MessageTopic.objects.all()
    context = {
        'topics': topics,
    }
    return render(request, 'community/community_topics.html', context)


@login_required
def view_topic(request, topic_id):
    """ A view to show individual topic posts """
    topic = get_object_or_404(MessageTopic, pk=topic_id)
    topic_messages = MessagePost.objects.filter(topic__subject=topic)

    template = 'community/view_topic.html'
    context = {
        'topic': topic,
        'topic_messages': topic_messages,
    }
    return render(request, template, context)


@login_required
def reply_post(request, topic_id):
    topic = get_object_or_404(MessageTopic, pk=topic_id)
    topic_messages = MessagePost.objects.filter(topic__subject=topic)

    if request.method == 'POST':
        form = MessagePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('view_topic',  topic_id=topic_id)
    else:
        form = MessagePostForm()
    template = 'community/reply_topic.html'
    context = {
        'topic': topic,
        'topic_messages': topic_messages,
        'form': form,
    }
    return render(request, template, context)


@login_required
def edit_post(request, post_id, topic_id):
    post = get_object_or_404(MessagePost, pk=post_id)
    topic = get_object_or_404(MessageTopic, pk=topic_id)

    if request.method == 'POST':
        form = MessagePostForm(request.POST, instance=post)
        if form.is_valid():
            post_form = form.save(commit=False)
            # post_form.topic = topic
            # post_form.created_by = request.user
            post_form.save()
            return redirect('view_topic',  topic_id=topic_id)
    else:
        form = MessagePostForm(instance=post)
    template = 'community/edit_post.html'
    context = {
        'post': post,
        'form': form,
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
