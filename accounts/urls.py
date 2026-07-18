from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/employer/", views.employer_dashboard, name="employer_dashboard"),
    path("dashboard/jobseeker/", views.jobseeker_dashboard, name="jobseeker_dashboard"),
    path("reports/", views.reports_view, name="reports"),
    path("manage-users/", views.manage_users, name="manage_users"),
    path("manage-users/<int:user_id>/toggle-active/", views.toggle_user_active, name="toggle_user_active"),
    path("manage-users/<int:user_id>/change-role/", views.change_user_role, name="change_user_role"),
]