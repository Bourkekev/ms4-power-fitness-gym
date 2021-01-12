from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import MessageTopic, MessagePost
from .forms import MessageTopicForm, MessagePostForm


def community_topics(request):
    """ community_topics:

    * Lists the Topics on the community message board

    \n Args:
    1. request

    \n Returns:
    * Topics to community_topics.html template
    """
    topics = MessageTopic.objects.all().order_by('-last_update')
    context = {
        'topics': topics,
    }
    return render(request, 'community/community_topics.html', context)


@login_required
def view_topic(request, topic_id):
    """ view_topic:

    * A view to show individual topic posts

    \n Args:
    1. request
    2. topic_id

    \n Returns:
    * Selected topic and topic messages to view_topic.html template
    """
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
    """ reply_post:

    * A view to allow user to POST reply to a topic
    * If POST, submits the message from form

    \n Args:
    1. request
    2. topic_id

    \n Returns:
    * Selected topic, topic messages and MessagePostForm \
        to reply_topic.html template
    """
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
    """ edit_post:

    * A view to allow user to Edit a message
    * If POST, submits edit message from form

    \n Args:
    1. request
    2. post_id
    3. topic_id

    \n Returns:
    * Post, topic and MessagePostForm \
        to edit_post.html template
    """
    post = get_object_or_404(MessagePost, pk=post_id)
    topic = get_object_or_404(MessageTopic, pk=topic_id)

    if request.user == post.created_by:
        if request.method == 'POST':
            form = MessagePostForm(request.POST, instance=post)
            if form.is_valid():
                post_form = form.save(commit=False)
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
    else:
        messages.error(request, 'This is not your post, you cannot edit it.')
        return redirect('view_topic',  topic_id=topic_id)
    return render(request, template, context)


@login_required
def delete_post(request, post_id, topic_id):
    """ delete_post:

    * Deletes the selected message

    \n Args:
    1. request
    2. post_id
    3. topic_id

    \n Returns:
    * User back to Topic (view_topic view)
    """
    post = get_object_or_404(MessagePost, pk=post_id)
    if request.user == post.created_by:
        post.delete()
        messages.success(request, 'Message deleted!')
        return redirect('view_topic',  topic_id=topic_id)
    else:
        messages.error(request, 'This is not your post, you cannot delete it.')
        return redirect('view_topic',  topic_id=topic_id)


@login_required
def add_topic(request):
    """ add_topic:

    * Adds a new Topic and the first message

    \n Args:
    1. request

    \n Returns:
    * User back to Community message board (community_topics view)
    """
    if request.method == 'POST':
        form = MessageTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.started_by = request.user
            topic.save()
            first_post = MessagePost.objects.create(
                message=form.cleaned_data['first_message'],
                topic=topic,
                created_by=request.user,
            )
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
