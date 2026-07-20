from django.urls import path
from . import views

urlpatterns = [
    # Employer
    path("post/", views.post_job, name="post_job"),
    path("my-jobs/", views.my_jobs, name="my_jobs"),
    path("<int:job_id>/edit/", views.edit_job, name="edit_job"),
    path("<int:job_id>/delete/", views.delete_employer_job, name="delete_employer_job"),
    path("<int:job_id>/applicants/", views.job_applicants, name="job_applicants"),
    path("application/<int:application_id>/update-status/", views.update_application_status, name="update_application_status"),


    # Admin
    path("manage/", views.manage_jobs, name="manage_jobs"),
    path("manage/<int:job_id>/toggle-active/", views.toggle_job_active, name="toggle_job_active"),
    path("manage/<int:job_id>/delete/", views.delete_job, name="delete_job"),
    path("applications/", views.view_all_applications, name="view_all_applications"),


    # Job Seeker
    path("", views.job_list, name="job_list"),
    path("<int:job_id>/", views.job_detail, name="job_detail"),
    path("<int:job_id>/apply/", views.apply_job, name="apply_job"),
    path("<int:job_id>/toggle-save/", views.toggle_save_job, name="toggle_save_job"),
    path("saved/", views.saved_jobs_list, name="saved_jobs_list"),
    path("my-applications/", views.my_applications, name="my_applications"),


    
]
