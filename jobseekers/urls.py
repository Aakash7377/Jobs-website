from django.urls import path
from . import views

urlpatterns = [
    path("setup/", views.profile_setup, name="jobseeker_profile_setup"),
]