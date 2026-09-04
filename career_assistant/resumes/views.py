from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Resume
from .forms import ResumeUploadForm
from .analyzer import analyze_resume
from jobs.models import Job, Application


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
    "node.js": 2,

    "django": 3,
    "flask": 3,
    "kubernetes": 3,
    "aws": 3,
    "azure": 3,
    "devops": 3
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


@login_required
def dashboard(request):

    if hasattr(request.user, "profile") and request.user.profile.role == "recruiter":
        return redirect("recruiter_dashboard")

    user_resumes = Resume.objects.filter(user=request.user).order_by("-uploaded_at")

    latest = user_resumes.first()

    avg_score = user_resumes.aggregate(avg=Avg("resume_score"))["avg"] or 0

    applications = Application.objects.filter(user=request.user)

    total_applied = applications.count()

    matched_jobs = 0

    if latest:

        user_skills = set(s.lower() for s in latest.get_detected_skills())

        if user_skills:

            for job in Job.objects.all():

                job_skills = set(
                    s.strip().lower() for s in job.skills.split(",") if s.strip()
                )

                if job_skills and len(user_skills & job_skills) / len(job_skills) >= 0.3:
                    matched_jobs += 1

    context = {
        "resumes": user_resumes,
        "latest_resume": latest,
        "avg_score": round(avg_score),
        "matched_jobs": matched_jobs,
        "total_applied": total_applied,
        "total_resumes": user_resumes.count(),
    }

    return render(request, "resumes/dashboard.html", context)


@login_required
def upload_resume(request):

    if hasattr(request.user, "profile") and request.user.profile.role == "recruiter":
        messages.error(request, "This feature is for job seekers only.")
        return redirect("recruiter_dashboard")

    if request.method == "POST":

        form = ResumeUploadForm(request.POST, request.FILES)

        if form.is_valid():

            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()

            result = analyze_resume(resume.uploaded_file.path)

            resume.extracted_text = result["extracted_text"]
            resume.resume_score = result["resume_score"]
            resume.detected_skills = ", ".join(result["detected_skills"])
            resume.detected_education = ", ".join(result["detected_education"])
            resume.detected_experience = ", ".join(result["detected_experience"])
            resume.missing_skills = ", ".join(result["missing_skills"])
            resume.suggestions = " | ".join(result["suggestions"])
            resume.formatting_score = result["formatting_score"]

            resume.save()

            messages.success(request, "Resume uploaded and analyzed successfully!")

            return redirect("resume_report", pk=resume.pk)

        else:

            messages.error(request, "Please upload a valid PDF or DOCX file.")

    else:

        form = ResumeUploadForm()

    return render(request, "resumes/upload.html", {"form": form})


@login_required
def resume_report(request, pk):

    resume = get_object_or_404(Resume, pk=pk, user=request.user)

    detected_skills = resume.get_detected_skills()
    missing_skills = resume.get_missing_skills()
    print("Missing skills:", missing_skills)

    # Certification links
    certifications = []
    for skill in missing_skills:

        query = skill.replace(" ", "+")

        certifications.append({
            "skill": skill,
            "coursera": f"https://www.coursera.org/search?query={query}",
            "udemy": f"https://www.udemy.com/courses/search/?q={query}&price=price-free"
        })


    # Learning Path
    learning_path = []
    for i, skill in enumerate(missing_skills):

        learning_path.append({
            "step": i + 1,
            "skill": skill,
            "course": f"https://www.coursera.org/search?query={skill}"
        })


    context = {
        "resume": resume,
        "detected_skills": detected_skills,
        "missing_skills": missing_skills,
        "certifications": certifications,
        "learning_path": learning_path,
        "education": resume.get_detected_education(),
        "experience": resume.get_detected_experience(),
        "suggestions": resume.get_suggestions(),
    }

    return render(request, "resumes/report.html", context)