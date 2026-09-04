
from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    JOB_TYPES = [("full-time", "Full Time"), ("part-time", "Part Time"),
                 ("contract", "Contract"), ("internship", "Internship"), ("remote", "Remote")]
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    salary = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default="full-time")
    experience = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    skills = models.TextField(help_text="Comma-separated skills")
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

    def get_skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(",") if s.strip()]

class Application(models.Model):
    STATUS_CHOICES = [("applied", "Applied"), ("reviewed", "Reviewed"),
                      ("shortlisted", "Shortlisted"), ("rejected", "Rejected")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.ForeignKey("resumes.Resume", on_delete=models.SET_NULL, null=True, blank=True)
    match_score = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "job")

    def __str__(self):
        return f"{self.user.username} -> {self.job.title}"
