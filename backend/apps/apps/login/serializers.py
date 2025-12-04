from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import SessionActivity, User, UserRole


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, max_length=128)

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "password",
            "role",
            "avatar_url",
            "bio",
        ]

    def validate_email(self, value: str) -> str:
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_("Email đã tồn tại trong hệ thống."))
        return email

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class RoleSelectSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=["student", "tutor", "admin"],
        error_messages={"invalid_choice": "Vai trò không hợp lệ."},
    )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=["student", "tutor", "admin"])
    remember_me = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"].lower())
        except User.DoesNotExist:
            raise serializers.ValidationError(_("Email không tồn tại."))

        if not user.check_password(attrs["password"]):
            raise serializers.ValidationError(_("Mật khẩu không đúng."))

        if not user.is_active:
            raise serializers.ValidationError(_("Tài khoản đã bị khóa."))

        attrs["user"] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True) 
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "role",
            "avatar_url",
            "bio",
            "last_login",
        ]
        
        read_only_fields = ["email", "last_login"]

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name", "avatar_url", "bio"]


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, attrs):
        user: User = self.context["request"].user
        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError(_("Mật khẩu hiện tại không đúng."))
        return attrs


class SessionActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionActivity
        fields = ["id", "ip_address", "user_agent", "created_at", "terminated_at"]


