from django import forms
from .models import Job, Application


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "description", "location", "job_type", "category", "experience", "salary_min", "salary_max", "deadline"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "job_type": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "experience": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 2-4 years"}),
            "salary_min": forms.NumberInput(attrs={"class": "form-control"}),
            "salary_max": forms.NumberInput(attrs={"class": "form-control"}),
            "deadline": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["cover_letter"]
        widgets = {
            "cover_letter": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Tell the employer why you're a great fit for this role..."}),
        }