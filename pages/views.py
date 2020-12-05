from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import ContactUsForm


class HomePageView(TemplateView):
    template_name = 'pages/index.html'


class GymMemberships(TemplateView):
    template_name = 'pages/gym-memberships.html'


def contact(request):

    if request.method == 'POST':
        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'subject': request.POST['subject'],
            'your_message': request.POST['your_message'],
        }
        contact_form = ContactUsForm(form_data)
        if contact_form.is_valid():
            contact_form.save()

    else:
        contact_form = ContactUsForm()

    context = {
        'contact_form': contact_form,
    }
    template = 'pages/contact.html'
    return render(request, template, context)
