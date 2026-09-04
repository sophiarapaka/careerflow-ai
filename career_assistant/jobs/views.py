from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Job, Application
from .forms import JobPostForm
from resumes.models import Resume


# ------------------------------
# Skill difficulty levels
# ------------------------------
SKILL_LEVELS = {
    "python": 1,
    "sql": 1,
    "html": 1,
    "css": 1,

    "docker": 2,
    "git": 2,
    "linux": 2,
    "terraform": 2,

    "kubernetes": 3,
    "aws": 3,
    "azure": 3,
    "devops": 3,
    "ci/cd": 3,
    "microservices": 3
}


def generate_learning_path(missing_skills):

    sorted_skills = sorted(
        missing_skills,
        key=lambda s: SKILL_LEVELS.get(s.lower(), 2)
    )

    learning_path = []

    for i, skill in enumerate(sorted_skills):
        learning_path.append({
            "step": i + 1,
            "skill": skill,
            "course": f"https://www.coursera.org/search?query={skill}"
        })

    return learning_path


def recruiter_required(view_func):
    """Decorator: only allow recruiters."""
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, "profile") or request.user.profile.role != "recruiter":
            messages.error(request, "Access denied. Recruiter account required.")
            return redirect("dashboard")
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return login_required(wrapper)


def jobseeker_required(view_func):
    """Decorator: only allow jobseekers."""
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, "profile") and request.user.profile.role == "recruiter":
            messages.error(request, "This feature is for job seekers only.")
            return redirect("recruiter_dashboard")
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return login_required(wrapper)


# ───────── RECRUITER VIEWS ─────────

@recruiter_required
def recruiter_dashboard(request):

    my_jobs = Job.objects.filter(posted_by=request.user).order_by("-created_at")

    total_jobs = my_jobs.count()
    active_jobs = my_jobs.filter(is_active=True).count()

    total_applications = Application.objects.filter(
        job__posted_by=request.user
    ).count()

    avg_match = Application.objects.filter(
        job__posted_by=request.user
    ).aggregate(avg=Avg("match_score"))["avg"] or 0

    recent_applications = Application.objects.filter(
        job__posted_by=request.user
    ).select_related("user", "job", "resume").order_by("-applied_at")[:10]

    context = {
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "total_applications": total_applications,
        "avg_match": round(avg_match),
        "my_jobs": my_jobs[:5],
        "recent_applications": recent_applications,
    }

    return render(request, "jobs/recruiter_dashboard.html", context)


@recruiter_required
def post_job(request):

    if request.method == "POST":

        form = JobPostForm(request.POST)

        if form.is_valid():

            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()

            messages.success(request, f'Job "{job.title}" posted successfully!')

            return redirect("my_posted_jobs")

        else:

            messages.error(request, "Please correct the errors below.")

    else:

        form = JobPostForm()

    return render(request, "jobs/post_job.html", {"form": form})


@recruiter_required
def my_posted_jobs(request):

    jobs = Job.objects.filter(posted_by=request.user).order_by("-created_at")

    job_data = []

    for job in jobs:

        app_count = Application.objects.filter(job=job).count()

        job_data.append({
            "job": job,
            "app_count": app_count,
            "skills": job.get_skills_list()
        })

    return render(request, "jobs/my_posted_jobs.html", {"job_data": job_data})


@recruiter_required
def edit_job(request, pk):

    job = get_object_or_404(Job, pk=pk, posted_by=request.user)

    if request.method == "POST":

        form = JobPostForm(request.POST, instance=job)

        if form.is_valid():

            form.save()
            messages.success(request, "Job updated successfully!")

            return redirect("my_posted_jobs")

    else:

        form = JobPostForm(instance=job)

    return render(request, "jobs/post_job.html", {"form": form, "editing": True, "job": job})


@recruiter_required
def toggle_job(request, pk):

    job = get_object_or_404(Job, pk=pk, posted_by=request.user)

    job.is_active = not job.is_active
    job.save()

    status = "activated" if job.is_active else "deactivated"

    messages.success(request, f'Job "{job.title}" {status}.')

    return redirect("my_posted_jobs")


@recruiter_required
def job_applications(request, pk):

    job = get_object_or_404(Job, pk=pk, posted_by=request.user)

    applications = Application.objects.filter(
        job=job
    ).select_related("user", "resume").order_by("-match_score")

    min_score = request.GET.get("min_score", "")
    skill_filter = request.GET.get("skill", "")

    if min_score:
        try:
            applications = applications.filter(match_score__gte=int(min_score))
        except ValueError:
            pass

    job_skills = job.get_skills_list()
    job_skills_lower = [s.lower() for s in job_skills]

    app_data = []

    for app in applications:

        user_skills = app.resume.get_detected_skills() if app.resume else []

        if skill_filter:
            if not any(skill_filter.lower() in s.lower() for s in user_skills):
                continue

        # ---------- SKILL GAP CALCULATION ----------
        user_skills_set = set([s.lower() for s in user_skills])

        missing_skills = [
            s for s in job_skills
            if s.lower() not in user_skills_set
        ]
        # ------------------------------------------

        app_data.append({
            "application": app,
            "user_skills": user_skills,
            "education": app.resume.get_detected_education() if app.resume else [],
            "experience": app.resume.get_detected_experience() if app.resume else [],
            "score": app.resume.resume_score if app.resume else 0,
            "missing_skills": missing_skills
        })

    context = {
        "job": job,
        "app_data": app_data,
        "total": len(app_data),
        "min_score": min_score,
        "skill_filter": skill_filter,
        "job_skills": job_skills,
        "job_skills_lower": job_skills_lower
    }

    return render(request, "jobs/job_applications.html", context)


@recruiter_required
def update_application_status(request, pk, status):

    valid = ["reviewed", "shortlisted", "rejected"]

    if status not in valid:

        messages.error(request, "Invalid status.")

        return redirect("recruiter_dashboard")

    app = get_object_or_404(Application, pk=pk, job__posted_by=request.user)

    app.status = status
    app.save()

    messages.success(request, f"Application marked as {status}.")

    return redirect("job_applications", pk=app.job.pk)


# ───────── JOB SEEKER VIEWS ─────────

@jobseeker_required
def job_list(request):

    jobs = Job.objects.filter(is_active=True).order_by("-created_at")

    q = request.GET.get("q", "")
    location = request.GET.get("location", "")
    job_type = request.GET.get("job_type", "")

    if q:
        jobs = jobs.filter(
            Q(title__icontains=q) |
            Q(company__icontains=q) |
            Q(skills__icontains=q)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    latest_resume = Resume.objects.filter(user=request.user).order_by("-uploaded_at").first()

    user_skills = set()

    if latest_resume:
        user_skills = set(s.lower() for s in latest_resume.get_detected_skills())

    job_data = []

    for job in jobs:

        job_skills = set(
            s.strip().lower() for s in job.skills.split(",") if s.strip()
        )

        match_pct = int(len(user_skills & job_skills) / len(job_skills) * 100) if job_skills and user_skills else 0

        job_data.append({
            "job": job,
            "skills": job.get_skills_list(),
            "match": match_pct
        })

    context = {
        "job_data": job_data,
        "q": q,
        "location": location,
        "job_type": job_type,
        "locations": list(Job.objects.values_list("location", flat=True).distinct()[:20]),
    }

    return render(request, "jobs/job_list.html", context)


@jobseeker_required
def job_detail(request, pk):

    job = get_object_or_404(Job, pk=pk)

    has_applied = Application.objects.filter(user=request.user, job=job).exists()

    latest_resume = Resume.objects.filter(user=request.user).order_by("-uploaded_at").first()

    user_skills = set()

    if latest_resume:
        user_skills = set(s.lower() for s in latest_resume.get_detected_skills())

    job_skills = job.get_skills_list()

    matching = [s for s in job_skills if s.lower() in user_skills]

    missing = [s for s in job_skills if s.lower() not in user_skills]

    match_pct = int(len(matching) / len(job_skills) * 100) if job_skills else 0


    # Certifications
    certifications = []

    for skill in missing:

        query = skill.replace(" ", "+")

        certifications.append({
            "skill": skill,
            "coursera": f"https://www.coursera.org/search?query={query}",
            "udemy": f"https://www.udemy.com/courses/search/?q={query}&price=price-free"
        })


    # Learning Path
    learning_path = generate_learning_path(missing)


    context = {
        "job": job,
        "job_skills": job_skills,
        "matching_skills": matching,
        "missing_skills": missing,
        "match_pct": match_pct,
        "certifications": certifications,
        "learning_path": learning_path,
        "has_applied": has_applied,
        "has_resume": latest_resume is not None,
    }

    return render(request, "jobs/job_detail.html", context)


@jobseeker_required
def apply_job(request, pk):

    job = get_object_or_404(Job, pk=pk)

    if Application.objects.filter(user=request.user, job=job).exists():

        messages.info(request, "You have already applied for this job.")

        return redirect("job_detail", pk=pk)

    latest_resume = Resume.objects.filter(user=request.user).order_by("-uploaded_at").first()

    if not latest_resume:

        messages.warning(request, "Please upload your resume before applying.")

        return redirect("upload_resume")

    user_skills = set(s.lower() for s in latest_resume.get_detected_skills())

    job_skills = set(
        s.strip().lower() for s in job.skills.split(",") if s.strip()
    )

    match_score = int(len(user_skills & job_skills) / len(job_skills) * 100) if job_skills else 0

    Application.objects.create(
        user=request.user,
        job=job,
        resume=latest_resume,
        match_score=match_score
    )

    messages.success(request, f"Applied to {job.title} successfully!")

    return redirect("job_detail", pk=pk)