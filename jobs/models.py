from django.db import models
from django.conf import settings
from companies.models import Company


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("internship", "Internship"),
        ("remote", "Remote"),
    ]

    CATEGORY_CHOICES = [
        ("it", "IT / Software"),
        ("marketing", "Marketing"),
        ("sales", "Sales"),
        ("finance", "Finance"),
        ("hr", "Human Resources"),
        ("design", "Design"),
        ("customer_support", "Customer Support"),
        ("other", "Other"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default="full_time")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="other")
    experience = models.CharField(max_length=100, blank=True, help_text="e.g. 2-4 years, Fresher")
    salary_min = models.PositiveIntegerField(blank=True, null=True)
    salary_max = models.PositiveIntegerField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"


class Application(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "applicant")

    def __str__(self):
        return f"{self.applicant.username} -> {self.job.title}"
    
class SavedJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="saved_by")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_jobs")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "user")

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"