
from django import forms
from .models import Resume

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["uploaded_file"]
        widgets = {
            "uploaded_file": forms.FileInput(attrs={
                "class": "form-control",
                "accept": ".pdf,.docx",
            })
        }
