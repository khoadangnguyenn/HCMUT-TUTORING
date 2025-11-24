from django.urls import path

from .views import PasswordResetConfirmView, PasswordResetRequestView

app_name = "forgetpassword"

urlpatterns = [
    path("request/", PasswordResetRequestView.as_view(), name="request"),
    path("confirm/", PasswordResetConfirmView.as_view(), name="confirm"),
]


