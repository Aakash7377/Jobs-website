from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import JobSeekerProfileForm
from .models import JobSeekerProfile


@login_required
def profile_setup(request):
    if request.user.role != "job_seeker":
        messages.error(request, "Only job seekers can access this page.")
        return redirect("employer_dashboard")

    profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("jobseeker_dashboard")
    else:
        form = JobSeekerProfileForm(instance=profile)

    return render(request, "jobseekers/profile_setup.html", {"form": form})