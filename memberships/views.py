from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def membership_dashboard(request):
    return render(request, 'memberships/memberships-dashboard.html')
