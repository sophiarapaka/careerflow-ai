from django.urls import path
from . import views

urlpatterns = [
    # Job seeker
    path("", views.job_list, name="job_list"),
    path("<int:pk>/", views.job_detail, name="job_detail"),
    path("<int:pk>/apply/", views.apply_job, name="apply_job"),
    # Recruiter
    path("recruiter/dashboard/", views.recruiter_dashboard, name="recruiter_dashboard"),
    path("recruiter/post/", views.post_job, name="post_job"),
    path("recruiter/my-jobs/", views.my_posted_jobs, name="my_posted_jobs"),
    path("recruiter/edit/<int:pk>/", views.edit_job, name="edit_job"),
    path("recruiter/toggle/<int:pk>/", views.toggle_job, name="toggle_job"),
    path("recruiter/applications/<int:pk>/", views.job_applications, name="job_applications"),
    path("recruiter/application/<int:pk>/status/<str:status>/", views.update_application_status, name="update_application_status"),
]
