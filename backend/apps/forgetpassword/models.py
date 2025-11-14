from datetime import timedelta
from uuid import uuid4

from django.db import models
from django.utils import timezone

from apps.login.models import User


def default_expiration():
    return timezone.now() + timedelta(minutes=30)


def generate_token():
    return uuid4().hex


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reset_requests")
    token = models.CharField(max_length=64, unique=True, default=generate_token)
    expires_at = models.DateTimeField(default=default_expiration)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    def mark_used(self):
        self.is_used = True
        self.save(update_fields=["is_used"])


