from django import forms
from .models import Job

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "company", "location", "salary", "job_type", "experience", "description", "requirements", "skills"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Python Developer"}),
            "company": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. TCS"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Hyderabad, India"}),
            "salary": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. ₹6,00,000 - ₹10,00,000"}),
            "job_type": forms.Select(attrs={"class": "form-select"}),
            "experience": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 1-3 years"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Job description..."}),
            "requirements": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Requirements..."}),
            "skills": forms.TextInput(attrs={"class": "form-control", "placeholder": "Python, Django, SQL (comma-separated)"}),
        }
