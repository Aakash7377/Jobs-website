from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from .models import User

from companies.models import Company
from jobs.models import Job, Application


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect_based_on_role(user)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect_based_on_role(user)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


# def redirect_based_on_role(user):
#     if user.role == User.ADMIN:
#         return redirect("admin_dashboard")
#     elif user.role == User.EMPLOYER:
#         return redirect("employer_dashboard")
#     else:
#         return redirect("jobseeker_dashboard")

def redirect_based_on_role(user):
    if user.role == User.ADMIN:
        return redirect("admin_dashboard")
    elif user.role == User.EMPLOYER:
        if hasattr(user, "company"):
            return redirect("employer_dashboard")
        return redirect("company_setup")
    else:
        return redirect("jobseeker_dashboard")
    

from django.contrib.auth.decorators import login_required


@login_required
def admin_dashboard(request):
    return render(request, "accounts/dashboard.html", {"role": "Admin"})


@login_required
def employer_dashboard(request):
    return render(request, "accounts/dashboard.html", {"role": "Employer"})


@login_required
def jobseeker_dashboard(request):
    return render(request, "accounts/dashboard.html", {"role": "Job Seeker"})


# Manage Users

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404


def is_admin(user):
    return user.is_authenticated and user.role == "admin"


@login_required
@user_passes_test(is_admin, login_url="jobseeker_dashboard")
def manage_users(request):
    role_filter = request.GET.get("role", "")
    users = User.objects.exclude(id=request.user.id).order_by("-date_joined")

    if role_filter:
        users = users.filter(role=role_filter)

    return render(request, "accounts/manage_users.html", {
        "users": users,
        "role_filter": role_filter,
    })


@login_required
@user_passes_test(is_admin, login_url="jobseeker_dashboard")
def toggle_user_active(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    target_user.is_active = not target_user.is_active
    target_user.save()
    messages.success(
        request,
        f"{target_user.username} has been {'activated' if target_user.is_active else 'deactivated'}."
    )
    return redirect("manage_users")


@login_required
@user_passes_test(is_admin, login_url="jobseeker_dashboard")
def change_user_role(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    new_role = request.POST.get("role")
    if new_role in dict(User.ROLE_CHOICES):
        target_user.role = new_role
        target_user.save()
        messages.success(request, f"{target_user.username}'s role changed to {target_user.get_role_display()}.")
    return redirect("manage_users")



# Reports

@login_required
@user_passes_test(is_admin, login_url="jobseeker_dashboard")
def reports_view(request):
    context = {
        "total_users": User.objects.count(),
        "total_job_seekers": User.objects.filter(role="job_seeker").count(),
        "total_employers": User.objects.filter(role="employer").count(),
        "total_admins": User.objects.filter(role="admin").count(),

        "total_companies": Company.objects.count(),
        "approved_companies": Company.objects.filter(is_approved=True).count(),
        "pending_companies": Company.objects.filter(is_approved=False).count(),

        "total_jobs": Job.objects.count(),
        "active_jobs": Job.objects.filter(is_active=True).count(),
        "inactive_jobs": Job.objects.filter(is_active=False).count(),

        "total_applications": Application.objects.count(),
        "pending_applications": Application.objects.filter(status="pending").count(),
        "shortlisted_applications": Application.objects.filter(status="shortlisted").count(),
        "rejected_applications": Application.objects.filter(status="rejected").count(),
    }
    return render(request, "accounts/reports.html", context)