from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from ..models import  Application,Job
from ..forms import JobForm

@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    # Sirf wahi employer status change kar sake jiski job hai
    if application.job.company.user != request.user:
        messages.error(request, "Access denied.")
        return redirect("my_jobs")

    new_status = request.POST.get("status")
    if new_status in dict(Application.STATUS_CHOICES):
        application.status = new_status
        application.save()
        messages.success(request, f"Application status updated to {application.get_status_display()}.")

    return redirect("job_applicants", job_id=application.job.id)


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.company.user != request.user:
        messages.error(request, "Access denied.")
        return redirect("my_jobs")

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully!")
            return redirect("my_jobs")
    else:
        form = JobForm(instance=job)

    return render(request, "jobs/edit_job.html", {"form": form, "job": job})


@login_required
def delete_employer_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.company.user != request.user:
        messages.error(request, "Access denied.")
        return redirect("my_jobs")

    job_title = job.title
    job.delete()
    messages.success(request, f"'{job_title}' has been deleted.")
    return redirect("my_jobs")