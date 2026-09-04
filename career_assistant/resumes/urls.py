
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("upload/", views.upload_resume, name="upload_resume"),
    path("report/<int:pk>/", views.resume_report, name="resume_report"),
]
