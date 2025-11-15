# from rest_framework.exceptions import AuthenticationFailed

# from .models import User


# def login_user(email: str, password: str, role: str) -> User:
#     """
#     ROLE-BASED LOGIN:
#     - role = student/tutor/admin
#     - user.is_student / user.is_tutor / user.is_admin
#     """

#     try:
#         user = User.objects.get(email=email.lower())
#     except User.DoesNotExist:
#         raise AuthenticationFailed("Sai email hoặc mật khẩu.")

#     # Check role-based login (nếu yêu cầu phân quyền)
#     if role == "student" and not getattr(user, "is_student", False):
#         raise AuthenticationFailed("Tài khoản không phải Student.")

#     if role == "tutor" and not getattr(user, "is_tutor", False):
#         raise AuthenticationFailed("Tài khoản không phải Tutor.")

#     if role == "admin" and not user.is_superuser:
#         raise AuthenticationFailed("Tài khoản không phải Admin.")

#     return user
# apps/login/services.py
from rest_framework.exceptions import AuthenticationFailed
from .models import User

def login_user(email: str, password: str, role: str) -> User:
    try:
        user = User.objects.get(email=email.lower())
    except User.DoesNotExist:
        # Chúng ta không nên nói rõ là sai email hay sai mật khẩu
        # vì lý do bảo mật, nhưng serializer của bạn đã làm vậy, 
        # nên chúng ta giữ nguyên logic của bạn
        raise AuthenticationFailed("Sai email hoặc mật khẩu.")

    # --- ĐÂY LÀ PHẦN SỬA LỖI LOGIC ---
    # So sánh 'role' (chuỗi) bạn gửi lên
    # với 'user.role' (chuỗi) trong database

    if role == "student" and user.role != "student":
        raise AuthenticationFailed("Tài khoản này không phải là Student.")

    if role == "tutor" and user.role != "tutor":
        raise AuthenticationFailed("Tài khoản này không phải là Tutor.")

    # Serializer của bạn nhận "admin"
    # Model của bạn lưu là "manager"
    if role == "admin" and user.role != "manager":
        raise AuthenticationFailed("Tài khoản này không phải là Ban Quản Lý.")

    # Hàm login_user trong service không cần check pass,
    # vì LoginSerializer đã check pass rồi.
    # Logic của bạn trong LoginAPI đang check pass 2 lần.
    # Nhưng chúng ta sẽ giữ nguyên, chỉ sửa lỗi role.
    return user