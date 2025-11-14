from bson import ObjectId
from bson.errors import InvalidId
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SessionActivity, User
from .serializers import (
    LoginSerializer,
    RoleSelectSerializer,
    SessionActivitySerializer,
    SignupSerializer,
    UpdateProfileSerializer,
    UserSerializer,
)
from .services import login_user


class LoginRoleAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        UI hiển thị 3 role:
        - SINH VIÊN
        - TUTOR
        - BAN QUẢN LÝ
        """
        roles = [
            {"key": "student", "label": "SINH VIÊN"},
            {"key": "tutor", "label": "TUTOR"},
            {"key": "admin", "label": "BAN QUẢN LÝ"},
        ]
        return Response({"roles": roles})

    def post(self, request):
        serializer = RoleSelectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"role": serializer.validated_data["role"]})


class LoginAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        role = serializer.validated_data["role"]
        remember = serializer.validated_data["remember_me"]

        try:
            user = login_user(email=email, password=password, role=role)
        except Exception as exc:  # pragma: no cover - service raises DRF errors
            return Response(
                {"success": False, "message": str(exc)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        self._persist_session(request, user, remember)

        redirect_map = {
            "student": "/home",
            "tutor": "/tutor/dashboard",
            "admin": "/admin/dashboard",
        }

        return Response(
            {
                "success": True,
                "message": "Log In success",
                "redirect_to": redirect_map.get(role, "/home"),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _persist_session(request, user, remember: bool) -> None:
        request.session["user_id"] = str(user.pk)
        request.session["role"] = user.role
        request.session["full_name"] = user.full_name

        session_activity = SessionActivity.objects.create(
            user=user,
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:255],
        )
        request.session["session_activity_id"] = str(session_activity.pk)

        if not remember:
            request.session.set_expiry(0)


class SessionUserMixin:
    def get_authenticated_user(self, request):
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

    def require_authentication(self, request):
        user = self.get_authenticated_user(request)
        if not user:
            return None, Response(
                {"detail": "Bạn cần đăng nhập trước khi tiếp tục."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return user, None


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    Đăng nhập dựa trên Session cho custom User (Mongo backend).
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data["user"]
        user.register_login()

        LoginAPI._persist_session(request, user, remember=True)

        return Response(
            {
                "message": "Đăng nhập thành công.",
                "user": UserSerializer(user).data,
            }
        )


class LogoutView(SessionUserMixin, APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = self.get_authenticated_user(request)
        activity_id = request.session.pop("session_activity_id", None)

        if activity_id:
            try:
                SessionActivity.objects.filter(pk=ObjectId(activity_id)).update(
                    terminated_at=timezone.now()
                )
            except InvalidId:
                pass

        request.session.flush()
        message = (
            "Đăng xuất thành công" if user else "Phiên đăng nhập đã kết thúc trước đó"
        )
        return Response({"message": message})


class ProfileView(SessionUserMixin, APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user, error = self.require_authentication(request)
        if error:
            return error
        return Response(UserSerializer(user).data)

    def patch(self, request):
        user, error = self.require_authentication(request)
        if error:
            return error

        serializer = UpdateProfileSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        request.session["full_name"] = user.full_name
        return Response(UserSerializer(user).data)


class SessionView(SessionUserMixin, APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = self.get_authenticated_user(request)
        if not user:
            return Response({"authenticated": False})
        return Response(
            {
                "authenticated": True,
                "user": UserSerializer(user).data,
            }
        )


class SessionActivityView(SessionUserMixin, APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user, error = self.require_authentication(request)
        if error:
            return error

        queryset = user.sessions.all()[:10]
        serializer = SessionActivitySerializer(queryset, many=True)
        return Response(serializer.data)

