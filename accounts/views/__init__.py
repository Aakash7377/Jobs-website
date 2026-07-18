from .change_password import CustomPasswordChangeView, password_change_done
from .auth_views import register_view, login_view, logout_view, redirect_based_on_role
from .dashboard_views import admin_dashboard, employer_dashboard, jobseeker_dashboard
from .admin_views import manage_users, toggle_user_active, change_user_role, reports_view, is_admin
# from .password_views import CustomPasswordChangeView, password_change_done