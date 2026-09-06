from django.urls import path
from . import views 
from .views import CustomPasswordChangeView
from django.contrib.auth import views as auth_views

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
    path("password-change/", CustomPasswordChangeView.as_view(), name="password_change"),
    path("password-change/done/", views.password_change_done, name="password_change_done"),


 # Forgot Password (Django built-in views)
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html",
        email_template_name="accounts/password_reset_email.html",
        subject_template_name="accounts/password_reset_subject.txt",
    ), name="password_reset"),

    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"
    ), name="password_reset_confirm"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ), name="password_reset_complete"),
]


