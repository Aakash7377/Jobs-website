from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Job, SavedJob


@login_required
def toggle_save_job(request, job_id):
    if request.user.role != "job_seeker":
        messages.error(request, "Only job seekers can save jobs.")
        return redirect("job_list")

    job = get_object_or_404(Job, id=job_id, is_active=True, company__is_approved=True)
    saved, created = SavedJob.objects.get_or_create(job=job, user=request.user)

    if not created:
        saved.delete()
        messages.info(request, "Job removed from saved list.")
    else:
        messages.success(request, "Job saved successfully!")

    # Wapas usi page pe bhejo jahan se aaya tha
    next_url = request.POST.get("next") or request.GET.get("next") or "job_list"
    return redirect(next_url)


@login_required
def saved_jobs_list(request):
    if request.user.role != "job_seeker":
        messages.error(request, "Access denied.")
        return redirect("employer_dashboard")

    saved = SavedJob.objects.filter(user=request.user).select_related("job", "job__company")
    return render(request, "jobs/saved_jobs.html", {"saved": saved})