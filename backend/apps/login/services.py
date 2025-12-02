from rest_framework.exceptions import AuthenticationFailed
from .models import User

def login_user(email: str, password: str, role: str) -> User:
    try:
        user = User.objects.get(email=email.lower())
    except User.DoesNotExist:
        raise AuthenticationFailed("Sai email hoặc mật khẩu.")

    # Check password
    if not user.check_password(password):
        raise AuthenticationFailed("Sai email hoặc mật khẩu.")

    # Check if user is active
    if not user.is_active:
        raise AuthenticationFailed("Tài khoản đã bị khóa.")

    # Check role matches
    if role == "student" and user.role != "student":
        raise AuthenticationFailed("Tài khoản này không phải là Student.")

    if role == "tutor" and user.role != "tutor":
        raise AuthenticationFailed("Tài khoản này không phải là Tutor.")

    if role == "admin" and user.role != "manager":
        raise AuthenticationFailed("Tài khoản này không phải là Ban Quản Lý.")

    return user