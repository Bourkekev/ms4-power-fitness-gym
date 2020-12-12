from django import forms
from .models import MessageTopic, MessagePost


class MessageTopicForm(forms.ModelForm):
    class Meta:
        # which model and which fields
        model = MessageTopic
        fields = (
            'subject',
            )


class MessagePostForm(forms.ModelForm):
    class Meta:
        # which model and which fields
        model = MessagePost
        fields = (
            'message',
            )
