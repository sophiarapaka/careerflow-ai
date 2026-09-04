from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Resume(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")

    uploaded_file = models.FileField(
        upload_to="resumes/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "docx"])]
    )

    extracted_text = models.TextField(blank=True)

    resume_score = models.IntegerField(default=0)

    detected_skills = models.TextField(blank=True)

    detected_education = models.TextField(blank=True)

    detected_experience = models.TextField(blank=True)

    missing_skills = models.TextField(blank=True)

    suggestions = models.TextField(blank=True)

    formatting_score = models.IntegerField(default=0)

    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - Score: {self.resume_score}"


    # ------------------------------
    # Skill getters
    # ------------------------------

    def get_detected_skills(self):

        if not self.detected_skills:
            return []

        return [s.strip() for s in self.detected_skills.split(",") if s.strip()]


    def get_missing_skills(self):

        if not self.missing_skills:
            return []

        return [s.strip() for s in self.missing_skills.split(",") if s.strip()]


    def get_detected_education(self):

        if not self.detected_education:
            return []

        return [s.strip() for s in self.detected_education.split(",") if s.strip()]


    def get_detected_experience(self):

        if not self.detected_experience:
            return []

        return [s.strip() for s in self.detected_experience.split(",") if s.strip()]


    def get_suggestions(self):

        if not self.suggestions:
            return []

        return [s.strip() for s in self.suggestions.split("|") if s.strip()]


    # ------------------------------
    # Certification links generator
    # ------------------------------

    def get_certification_links(self):

        skills = self.get_missing_skills()

        certifications = []

        for skill in skills:

            query = skill.replace(" ", "+")

            certifications.append({
                "skill": skill,
                "coursera": f"https://www.coursera.org/search?query={query}",
                "udemy": f"https://www.udemy.com/courses/search/?q={query}&price=price-free"
            })

        return certifications