from django.db import models
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import ContactUsForm
from .models import ContactForm

from products.models import Product


class HomePageView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        products = Product.objects.all()
        best_sellers = products.filter(category__name='best_sellers')
        context["best_sellers"] = best_sellers
        return context


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
            return redirect(reverse('contact'))
        else:
            # if form not valid
            messages.error(request, 'There was an error with your form. \
                Please double check the information submitted.')

    else:
        contact_form = ContactUsForm()

    context = {
        'contact_form': contact_form,
    }
    template = 'pages/contact.html'
    return render(request, template, context)


def contact_submit(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        subject = request.POST['subject']
        your_message = request.POST['your_message']
        date_sent = models.DateTimeField(auto_now_add=True)

        ContactForm.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            subject=subject,
            your_message=your_message,
            date_sent=date_sent,
        )
        return HttpResponse('Your message has been submitted successfully.')
