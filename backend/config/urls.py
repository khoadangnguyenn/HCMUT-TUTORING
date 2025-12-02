from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from apps.home.views import HomeTemplateView

urlpatterns = [
    path("api/auth/", include("apps.login.urls")),
    path("api/password/", include(("apps.forgetpassword.urls", "forgetpassword"), namespace="password-api")),
    path("api/roles/", include("apps.roleselect.urls")),
    path("home/", include(("apps.home.urls", "home"), namespace="home")),
    path("", HomeTemplateView.as_view(), name="home"),
    path("roleselect/", TemplateView.as_view(template_name="roleselect/roleselect.html"), name="roleselect"),
    path("login/", TemplateView.as_view(template_name="login/login.html"), name="login"),
    path("forgetpassword/", TemplateView.as_view(template_name="forgetpassword/forgetpassword.html"), name="forgetpassword"),
    path("api/password-reset/", include(("apps.forgetpassword.urls", "forgetpassword"), namespace="password-reset")),
]
