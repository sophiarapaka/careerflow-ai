from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),

    # role selection
    path("select-role/", views.select_role, name="select_role"),

    # start google login with role
    path("start-google-login/<str:role>/", views.start_google_login, name="start_google_login"),
]