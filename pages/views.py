from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'pages/index.html'


class GymMemberships(TemplateView):
    template_name = 'pages/gym-memberships.html'


class ContactPage(TemplateView):
    template_name = 'pages/contact.html'
