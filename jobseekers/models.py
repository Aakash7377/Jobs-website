from django.db import models
from django.conf import settings


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobseeker_profile'
    )
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=500, blank=True, help_text="Comma separated skills, e.g. Python, Django, SQL")
    education = models.CharField(max_length=300, blank=True, help_text="e.g. B.Tech in Computer Science, XYZ University")
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"