from django.contrib.auth.views import PasswordChangeView,login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import  redirect

class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("password_change_done")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({"class": "form-control"})
        return form


@login_required
def password_change_done(request):
    messages.success(request, "Your password was changed successfully!")
    return redirect("jobseeker_dashboard" if request.user.role == "job_seeker"
                     else "employer_dashboard" if request.user.role == "employer"
                     else "admin_dashboard")