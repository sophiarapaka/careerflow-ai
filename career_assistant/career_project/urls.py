
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda r: redirect("dashboard"), name="home"),
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("resumes.urls")),
    path("jobs/", include("jobs.urls")),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
