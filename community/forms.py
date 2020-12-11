from django import forms
from .models import MessageTopic


class MessageTopicForm(forms.ModelForm):
    class Meta:
        # which model and which fields
        model = MessageTopic
        fields = (
            'subject',
            )
