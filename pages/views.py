from django.db import models
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .forms import ContactUsForm
from .models import ContactForm

from products.models import Product


class HomePageView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        products = Product.objects.all()
        best_sellers = products.filter(is_best_seller='True')
        context['best_sellers'] = best_sellers
        return context


class GymMemberships(TemplateView):
    template_name = 'pages/gym-memberships.html'


def contact(request):

    if request.method == 'POST':
        contact_form = ContactUsForm(request.POST)
        if contact_form.is_valid():
            # Send user email
            user_email = contact_form.cleaned_data['email']
            user_name = contact_form.cleaned_data['first_name']
            subject = ("Form Submission received: " +
                       contact_form.cleaned_data['subject'])
            body = render_to_string(
                'pages/contact_emails/contact_email_body.txt',
                {'contact_email': settings.DEFAULT_FROM_EMAIL})
            send_mail(
                subject,
                f"Hi {user_name}," + body,
                settings.DEFAULT_FROM_EMAIL,
                [user_email]
            )
            # Send admin email
            if settings.EMAIL_HOST_USER:
                admin_email = settings.EMAIL_HOST_USER
            else:
                admin_email = settings.DEFAULT_FROM_EMAIL

            last_name = contact_form.cleaned_data['last_name']
            phone_number = contact_form.cleaned_data['phone_number']
            your_message = contact_form.cleaned_data['your_message']
            admin_body = render_to_string(
                'pages/contact_emails/admin_email_body.txt',
                {
                    'sender_email': user_email,
                    'first_name': user_name,
                    'last_name': last_name,
                    'phone_number': phone_number,
                    'subject': subject,
                    'your_message': your_message,
                })
            send_mail(
                subject,
                admin_body,
                settings.DEFAULT_FROM_EMAIL,
                [admin_email]
            )
            contact_form.save()
            messages.success(request, 'Message sent successfully')
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
        # Send user email
        user_email = email
        subject = ("Form Submission received: " +
                   subject)
        body = render_to_string(
            'pages/contact_emails/contact_email_body.txt',
            {'contact_email': settings.DEFAULT_FROM_EMAIL})
        send_mail(
            subject,
            f"Hi {first_name}," + body,
            settings.DEFAULT_FROM_EMAIL,
            [user_email]
        )
        # Send admin email
        if settings.EMAIL_HOST_USER:
            admin_email = settings.EMAIL_HOST_USER
        else:
            admin_email = settings.DEFAULT_FROM_EMAIL

        admin_body = render_to_string(
            'pages/contact_emails/admin_email_body.txt',
            {
                'sender_email': user_email,
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'subject': subject,
                'your_message': your_message,
            })
        send_mail(
            subject,
            admin_body,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email]
        )
        return HttpResponse('Your message has been submitted successfully.')
