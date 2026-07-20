from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from ..models import Job, Application
from ..forms import ApplicationForm

@login_required
def apply_job(request, job_id):
    if request.user.role != "job_seeker":
        messages.error(request, "Only job seekers can apply.")
        return redirect("employer_dashboard")

    job = get_object_or_404(Job, id=job_id, is_active=True, company__is_approved=True)

    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, "You have already applied to this job.")
        return redirect("job_detail", job_id=job.id)

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect("job_detail", job_id=job.id)
    else:
        form = ApplicationForm()

    return render(request, "jobs/apply_job.html", {"job": job, "form": form})