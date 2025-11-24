from rest_framework.exceptions import AuthenticationFailed
from .models import User

def login_user(email: str, password: str, role: str) -> User:
    try:
        user = User.objects.get(email=email.lower())
    except User.DoesNotExist:
        raise AuthenticationFailed("Sai email hoặc mật khẩu.")

    if role == "student" and user.role != "student":
        raise AuthenticationFailed("Tài khoản này không phải là Student.")

    if role == "tutor" and user.role != "tutor":
        raise AuthenticationFailed("Tài khoản này không phải là Tutor.")

    return user