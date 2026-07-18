from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import JobForm
from .models import Job, Application
from django.db.models import Q


# ---------- EMPLOYER SIDE ----------

@login_required
def post_job(request):
    if request.user.role != "employer":
        messages.error(request, "Only employers can post jobs.")
        return redirect("jobseeker_dashboard")

    if not hasattr(request.user, "company"):
        messages.error(request, "Please set up your company first.")
        return redirect("company_setup")

    company = request.user.company
    if not company.is_approved:
        messages.error(request, "Your company is not approved yet. Please wait for admin approval.")
        return redirect("employer_dashboard")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect("my_jobs")
    else:
        form = JobForm()

    return render(request, "jobs/post_job.html", {"form": form})


@login_required
def my_jobs(request):
    if request.user.role != "employer" or not hasattr(request.user, "company"):
        messages.error(request, "Access denied.")
        return redirect("jobseeker_dashboard")

    jobs = Job.objects.filter(company=request.user.company)
    return render(request, "jobs/my_jobs.html", {"jobs": jobs})


@login_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.company.owner != request.user:
        messages.error(request, "Access denied.")
        return redirect("my_jobs")

    applications = job.applications.select_related("applicant")
    return render(request, "jobs/job_applicants.html", {"job": job, "applications": applications})


# ---------- JOB SEEKER SIDE ----------


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
    return render(request, "jobs/job_detail.html", {"job": job, "already_applied": already_applied})


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


# naye admin views

from django.contrib.auth.decorators import login_required, user_passes_test

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


# View Application

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