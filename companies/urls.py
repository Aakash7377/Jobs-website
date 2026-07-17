from django.urls import path
from . import views

urlpatterns = [
    path("setup/", views.company_setup, name="company_setup"),
]