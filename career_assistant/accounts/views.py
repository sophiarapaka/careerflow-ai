from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignupForm
from .models import Profile


def login_view(request):

    if request.user.is_authenticated:
        return redirect_by_role(request, request.user)

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()

            # specify backend because we have Google login also
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect_by_role(request, user)

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html", {"form": form})


def signup_view(request):

    if request.user.is_authenticated:
        return redirect_by_role(request, request.user)

    form = SignupForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            user = form.save()

            role = form.cleaned_data.get("role", "student")

            Profile.objects.create(
                user=user,
                role=role
            )

            # specify backend here also
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            messages.success(request, "Account created successfully!")

            return redirect_by_role(request, user)

        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, "accounts/signup.html", {"form": form})


def logout_view(request):

    logout(request)

    return redirect("login")


# ROLE SELECTION PAGE (before Google login)

def select_role(request):

    return render(request, "accounts/select_role.html")


# START GOOGLE LOGIN AFTER ROLE CHOICE

def start_google_login(request, role):

    request.session["google_role"] = role

    return redirect("/accounts/google/login/")


# REDIRECT USER BASED ON ROLE

def redirect_by_role(request, user):

    profile, created = Profile.objects.get_or_create(user=user)

    # if role already set
    if profile.role:

        if profile.role == "recruiter":
            return redirect("recruiter_dashboard")

        return redirect("dashboard")

    # check if role stored from Google login
    role = request.session.get("google_role")

    if role:

        profile.role = role
        profile.save()

        del request.session["google_role"]

        if role == "recruiter":
            return redirect("recruiter_dashboard")

        return redirect("dashboard")

    return redirect("dashboard")