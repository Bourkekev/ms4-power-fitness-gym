from django import forms
from .models import UserProfile


class EditUserProfile(forms.ModelForm):
    """
    Allows logged in users to edit their profile
    """
    class Meta:
        # which model and which fields
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_email': 'Email Address',
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County',
            'default_country': 'Country',
        }

        # auto focus on name field
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        # add star on required fields
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
            # set placeholder values
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # add stripe class
            self.fields[field].widget.attrs['class'] = 'profile-form'
            self.fields[field].label = False
