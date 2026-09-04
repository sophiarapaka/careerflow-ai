
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    role = forms.ChoiceField(choices=[("jobseeker", "Job Seeker"), ("recruiter", "Recruiter")])

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
