import re
from rest_framework.exceptions import ValidationError

def validate_email(email: str):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        raise ValidationError("Email không hợp lệ.")
    return email


def validate_password(password: str):
    if len(password) < 6:
        raise ValidationError("Mật khẩu phải ít nhất 6 ký tự.")
    if password.strip() != password:
        raise ValidationError("Mật khẩu không được chứa khoảng trắng ở đầu/cuối.")
    return password