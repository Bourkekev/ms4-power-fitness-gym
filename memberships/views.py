from django.shortcuts import render


def membership_dashboard(request):
    return render(request, 'memberships/memberships-dashboard.html')
