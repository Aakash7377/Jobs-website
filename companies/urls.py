from django.urls import path
from . import views

urlpatterns = [
    path("setup/", views.company_setup, name="company_setup"),
    path("manage/", views.manage_companies, name="manage_companies"),
    path("approve/<int:company_id>/", views.approve_company, name="approve_company"),
    path("reject/<int:company_id>/", views.reject_company, name="reject_company"),
]