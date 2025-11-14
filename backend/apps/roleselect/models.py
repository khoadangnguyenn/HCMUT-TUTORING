from django.db import models

from apps.login.models import User, UserRole


class RoleOption(models.Model):
    code = models.CharField(
        max_length=20,
        unique=True,
        choices=UserRole.choices,
    )
    label = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.label


class RoleSelectionLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="role_logs",
    )
    role = models.CharField(max_length=20, choices=UserRole.choices)
    source = models.CharField(max_length=50, default="manual")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


