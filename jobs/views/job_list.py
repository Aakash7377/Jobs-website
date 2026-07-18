from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from ..models import Job, SavedJob



@login_required
def job_list(request):
    jobs = Job.objects.filter(is_active=True, company__is_approved=True).select_related("company")

    query = request.GET.get("q", "").strip()
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | Q(company__name__icontains=query)
        )

    location = request.GET.get("location", "").strip()
    if location:
        jobs = jobs.filter(location__icontains=location)

    job_type = request.GET.get("job_type", "").strip()
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    # Filter dropdown ke liye unique locations nikaalo
    all_locations = Job.objects.filter(
        is_active=True, company__is_approved=True
    ).values_list("location", flat=True).distinct()

    saved_job_ids = []
    if request.user.role == "job_seeker":
        saved_job_ids = list(SavedJob.objects.filter(user=request.user).values_list("job_id", flat=True))

    return render(request, "jobs/job_list.html", {
        "jobs": jobs,
        "query": query,
        "location": location,
        "job_type": job_type,
        "all_locations": all_locations,
        "job_type_choices": Job.JOB_TYPE_CHOICES,
    })