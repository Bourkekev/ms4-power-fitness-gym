from django import forms
from .models import ContactForm


class ContactUsForm(forms.ModelForm):
    """
    Creates the Contact Us form.
    It will not include date or answered fields.
    """
    class Meta:
        # which model and which fields
        model = ContactForm
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'subject',
            'your_message',
            )
