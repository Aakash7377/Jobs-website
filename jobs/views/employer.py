from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..forms import JobForm
from ..models import Job


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
    if job.company.user != request.user:
        messages.error(request, "Access denied.")
        return redirect("my_jobs")

    applications = job.applications.select_related("applicant")
    return render(request, "jobs/job_applicants.html", {"job": job, "applications": applications})