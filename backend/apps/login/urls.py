from django.urls import path

from .views import (
    LoginAPI,
    LoginRoleAPI,
    LoginView,
    LogoutView,
    ProfileView,
    SessionActivityView,
    SessionView,
    SignupView,
)

app_name = "login"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("roles/", LoginRoleAPI.as_view(), name="select_role"),
    path("login/", LoginAPI.as_view(), name="login_api"),
    path("session/login/", LoginView.as_view(), name="session_login"),
    path("session/", SessionView.as_view(), name="session"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("activity/", SessionActivityView.as_view(), name="activity"),
    path("logout/", LogoutView.as_view(), name="logout"),
]