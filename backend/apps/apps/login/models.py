from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone
from django.templatetags.static import static


class UserRole(models.TextChoices):
    STUDENT = "student", "Sinh viên"
    TUTOR = "tutor", "Tutor"
    MANAGER = "manager", "Ban quản lý"


class User(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
    )
    avatar_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def set_password(self, raw_password: str) -> None:
        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password)

    def register_login(self) -> None:
        self.last_login = timezone.now()
        self.save(update_fields=["last_login"])

    def get_avatar_url(self) -> str:
        """Get avatar URL, with fallback based on role"""
        if self.avatar_url:
            return self.avatar_url
        avatar_map = {
            'student': static('home/resources/student-avatar.jpg'),
            'tutor': static('home/resources/tutor-avatar.jpg'),
            'manager': static('home/resources/manager-avatar.jpg'),
        }
        return avatar_map.get(self.role, static('home/resources/student-avatar.jpg'))

    def to_public_dict(self) -> dict:
        return {
            "id": str(self.pk),
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }


class SessionActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    terminated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def close(self) -> None:
        self.terminated_at = timezone.now()
        self.save(update_fields=["terminated_at"])


