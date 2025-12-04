from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.login.models import User

from .models import PasswordResetRequest


class PasswordResetRequestView(APIView):
    """
    Tạo yêu cầu đặt lại mật khẩu dựa trên email người dùng.
    """

    def post(self, request):
        email = request.data.get("email", "").lower()
        if not email:
            return Response(
                {"detail": "Vui lòng cung cấp email."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Trả về thành công để tránh lộ email
            return Response(
                {
                    "message": "Nếu email tồn tại, hướng dẫn khôi phục đã được gửi.",
                }
            )

        PasswordResetRequest.objects.create(user=user)
        latest_request = user.reset_requests.first()

        return Response(
            {
                "message": "Yêu cầu đặt lại mật khẩu đã được tạo.",
                "token": latest_request.token,
                "expires_at": latest_request.expires_at,
            }
        )


class PasswordResetConfirmView(APIView):
    """
    Xác nhận token và thay đổi mật khẩu.
    """

    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not token or not new_password:
            return Response(
                {"detail": "Thiếu token hoặc mật khẩu mới."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            reset_request = PasswordResetRequest.objects.get(token=token)
        except PasswordResetRequest.DoesNotExist:
            return Response(
                {"detail": "Token không hợp lệ."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if reset_request.is_used:
            return Response(
                {"detail": "Token đã được sử dụng."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if reset_request.is_expired:
            return Response(
                {"detail": "Token đã hết hạn."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = reset_request.user
        user.set_password(new_password)
        user.save(update_fields=["password"])
        reset_request.mark_used()

        return Response({"message": "Mật khẩu đã được cập nhật thành công."})


