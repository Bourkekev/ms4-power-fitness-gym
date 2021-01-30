from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .forms import ContactUsForm


class TestPagesForms(TestCase):
    def test_contact_form_validation_for_blank_fields(self):
        form = ContactUsForm(data={
            'first_name': '',
            'last_name': '',
            'email': '',
            'subject': '',
            'your_message': '',
            })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['first_name'],
            ["This field is required."]
        )
        self.assertEqual(
            form.errors['last_name'],
            ["This field is required."]
        )
        self.assertEqual(
            form.errors['email'],
            ["This field is required."]
        )
        self.assertEqual(
            form.errors['subject'],
            ["This field is required."]
        )
        self.assertEqual(
            form.errors['your_message'],
            ["This field is required."]
        )

    def test_contact_form_validation_filled_fields(self):
        form = ContactUsForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'email@example.com',
            'subject': 'Test contact form',
            'your_message': 'Test message here.',
            })
        self.assertTrue(form.is_valid())
        form.save()

    def test_contact_form_submission(self):
        response = self.client.post(reverse('contact'), {
            'first_name': 'Test First name',
            'last_name': 'Test last name',
            'email': 'contact@email.com',
            'phone_number': 'Phone number',
            'subject': 'Contact form test',
            'your_message': 'Test submitting contact form',
        })
        self.assertRedirects(response, '/contact/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        expected_message = ('Message sent successfully')
        self.assertEqual(messages[0].tags, 'success')
        self.assertEqual(str(messages[0]), expected_message)

    def test_contact_form_submit_not_valid(self):
        response = self.client.post(reverse('contact'), {
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone_number': '',
            'subject': '',
            'your_message': '',
        })
        messages = list(get_messages(response.wsgi_request))
        expected_message = ('There was an error with your form. \
                Please double check the information submitted.')
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(str(messages[0]), expected_message)

    def test_contact_submit_ajax_submission(self):
        response = self.client.post(reverse('contact_submit'), {
            'first_name': 'Test First name',
            'last_name': 'Test last name',
            'email': 'contact@email.com',
            'phone_number': 'Phone number',
            'subject': 'Contact form test',
            'your_message': 'Test submitting contact form',
        })
        self.assertEqual(response.content,
                         b'Your message has been submitted successfully.')
