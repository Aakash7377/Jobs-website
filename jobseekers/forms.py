from django import forms
from .models import JobSeekerProfile


# class JobSeekerProfileForm(forms.ModelForm):
#     class Meta:
#         model = JobSeekerProfile
#         fields = ["bio", "skills", "resume", "experience_years", "location"]

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ["bio", "skills", "education", "resume", "experience_years", "address","phone", "profile_image"]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "skills": forms.TextInput(attrs={"class": "form-control"}),
            "education": forms.TextInput(attrs={"class": "form-control"}),
            "resume": forms.FileInput(attrs={"class": "form-control"}),
            "experience_years": forms.NumberInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "profile_image": forms.FileInput(attrs={"class": "form-control"}),
        }