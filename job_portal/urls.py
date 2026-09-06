from django.contrib import admin
from django.urls import path, include
# from django.views.generic import RedirectView
from accounts.views import home_view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("company/", include("companies.urls")),
    path("jobseeker/", include("jobseekers.urls")),
    path("jobs/", include("jobs.urls")),
    # path("", RedirectView.as_view(url="accounts/login/", permanent=False)),
    path("", home_view, name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)