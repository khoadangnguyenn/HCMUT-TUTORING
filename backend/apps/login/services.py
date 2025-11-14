from rest_framework.exceptions import AuthenticationFailed

from .models import User


def login_user(email: str, password: str, role: str) -> User:
    """
    ROLE-BASED LOGIN:
    - role = student/tutor/admin
    - user.is_student / user.is_tutor / user.is_admin
    """

    try:
        user = User.objects.get(email=email.lower())
    except User.DoesNotExist:
        raise AuthenticationFailed("Sai email hoặc mật khẩu.")

    # Check role-based login (nếu yêu cầu phân quyền)
    if role == "student" and not getattr(user, "is_student", False):
        raise AuthenticationFailed("Tài khoản không phải Student.")

    if role == "tutor" and not getattr(user, "is_tutor", False):
        raise AuthenticationFailed("Tài khoản không phải Tutor.")

    if role == "admin" and not user.is_superuser:
        raise AuthenticationFailed("Tài khoản không phải Admin.")

    return user