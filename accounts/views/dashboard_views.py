from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def admin_dashboard(request):
    return render(request, "accounts/dashboard.html", {"role": "Admin"})


@login_required
def employer_dashboard(request):
    return render(request, "accounts/dashboard.html", {"role": "Employer"})


@login_required
def jobseeker_dashboard(request):
    return render(request, "accounts/dashboard.html", {"role": "Job Seeker"})

