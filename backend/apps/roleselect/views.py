from bson import ObjectId
from bson.errors import InvalidId
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.login.models import User, UserRole

from .models import RoleOption, RoleSelectionLog


def seed_roles():
    if RoleOption.objects.exists():
        return
    RoleOption.objects.bulk_create(
        [
            RoleOption(code=UserRole.STUDENT, label="Sinh viên"),
            RoleOption(code=UserRole.TUTOR, label="Tutor"),
            RoleOption(code=UserRole.MANAGER, label="Ban quản lý"),
        ]
    )


class RoleListView(APIView):
    def get(self, request):
        seed_roles()
        roles = RoleOption.objects.filter(is_active=True).values("code", "label", "description")
        return Response({"roles": list(roles)})


class RoleSelectionView(APIView):
    def post(self, request):
        seed_roles()
        role = request.data.get("role")
        if role not in dict(UserRole.choices):
            return Response(
                {"detail": "Vai trò không hợp lệ."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        option = RoleOption.objects.filter(code=role, is_active=True).first()
        if not option:
            return Response(
                {"detail": "Vai trò hiện không khả dụng."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = self._get_session_user(request)
        if user:
            user.role = role
            user.save(update_fields=["role"])

        request.session["role"] = role
        RoleSelectionLog.objects.create(
            user=user,
            role=role,
            source="session" if user else "anonymous",
        )

        return Response(
            {
                "message": "Cập nhật vai trò thành công.",
                "role": {
                    "code": option.code,
                    "label": option.label,
                },
            }
        )

    def _get_session_user(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            return None
        try:
            object_id = ObjectId(user_id)
        except InvalidId:
            return None
        try:
            return User.objects.get(pk=object_id)
        except User.DoesNotExist:
            return None


