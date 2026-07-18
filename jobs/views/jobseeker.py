from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from ..models import Job, Application, SavedJob


@login_required
def job_list(request):
    jobs = Job.objects.filter(is_active=True, company__is_approved=True).select_related("company")

    query = request.GET.get("q", "").strip()
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | Q(company__name__icontains=query)
        )

    return render(request, "jobs/job_list.html", {"jobs": jobs, "query": query})


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True, company__is_approved=True)
    already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    is_saved = SavedJob.objects.filter(job=job, user=request.user).exists() if request.user.role == "job_seeker" else False
    return render(request, "jobs/job_detail.html", {
        "job": job,
        "already_applied": already_applied,
        "is_saved": is_saved,
    })

@login_required
def apply_job(request, job_id):
    if request.user.role != "job_seeker":
        messages.error(request, "Only job seekers can apply.")
        return redirect("employer_dashboard")

    job = get_object_or_404(Job, id=job_id, is_active=True, company__is_approved=True)

    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, "You have already applied to this job.")
    else:
        Application.objects.create(job=job, applicant=request.user)
        messages.success(request, "Application submitted successfully!")

    return redirect("job_detail", job_id=job.id)


@login_required
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user).select_related("job", "job__company")
    return render(request, "jobs/my_applications.html", {"applications": applications})