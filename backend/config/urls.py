from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from apps.home.views import HomeTemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.login.urls")),
    path("api/password/", include("apps.forgetpassword.urls")),
    path("api/roles/", include("apps.roleselect.urls")),
    path("home/", include(("apps.home.urls", "home"), namespace="home")),
    path("", HomeTemplateView.as_view(), name="home"),
    path("login/", TemplateView.as_view(template_name="login/login.html"), name="login"),
    path("signup/", TemplateView.as_view(template_name="signup/signup.html"), name="signup"),
    path("signup_success/", TemplateView.as_view(template_name="signup_success/signup_success.html"), name="signup_success"),
    path("forgetpassword/", TemplateView.as_view(template_name="forgetpassword/forgetpassword.html"), name="forgetpassword"),
    path("api/password-reset/", include("apps.forgetpassword.urls")),
]