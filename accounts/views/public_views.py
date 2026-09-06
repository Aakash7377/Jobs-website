from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from jobs.models import Job


def home_view(request):
    latest_jobs = Job.objects.filter(
        is_active=True, company__is_approved=True
    ).select_related("company").order_by("-created_at")[:6]
    return render(request, "home.html", {"latest_jobs": latest_jobs})


def about_view(request):
    return render(request, "about.html")


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        send_mail(
            subject=f"Contact Form: {subject}",
            message=f"From: {name} ({email})\n\n{message}",
            from_email=None,
            recipient_list=["admin@jobportal.com"],
        )

        messages.success(request, "Your message has been sent! We'll get back to you soon.")
        return redirect("contact")

    return render(request, "contact.html")