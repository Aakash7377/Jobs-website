from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from ..models import Job, Application,SavedJob


def is_admin(user):
    return user.is_authenticated and user.role == "admin"


@login_required
@user_passes_test(is_admin, login_url="jobseeker_dashboard")
def manage_jobs(request):
    jobs = Job.objects.select_related("company").order_by("-created_at")
    return render(request, "jobs/manage_jobs.html", {"jobs": jobs})


@login_required
@user_passes_test(is_admin, login_url="jobseeker_dashboard")
def toggle_job_active(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.is_active = not job.is_active
    job.save()
    messages.success(request, f"'{job.title}' has been {'activated' if job.is_active else 'deactivated'}.")
    return redirect("manage_jobs")


@login_required
@user_passes_test(is_admin, login_url="jobseeker_dashboard")
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job_title = job.title
    job.delete()
    messages.success(request, f"'{job_title}' has been deleted.")
    return redirect("manage_jobs")


@login_required
@user_passes_test(is_admin, login_url="jobseeker_dashboard")
def view_all_applications(request):
    applications = Application.objects.select_related(
        "job", "job__company", "applicant"
    ).order_by("-applied_at")

    status_filter = request.GET.get("status", "")
    if status_filter:
        applications = applications.filter(status=status_filter)

    query = request.GET.get("q", "").strip()
    if query:
        applications = applications.filter(
            Q(job__title__icontains=query) |
            Q(job__company__name__icontains=query) |
            Q(applicant__username__icontains=query)
        )

    return render(request, "jobs/view_all_applications.html", {
        "applications": applications,
        "status_filter": status_filter,
        "query": query,
    })

