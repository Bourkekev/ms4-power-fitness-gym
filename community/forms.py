from django import forms
from .models import MessageTopic, MessagePost


class MessageTopicForm(forms.ModelForm):
    first_message = forms.CharField(widget=forms.Textarea(), max_length=4000)

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
