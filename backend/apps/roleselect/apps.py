from django.apps import AppConfig


class RoleSelectConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "apps.roleselect"
    verbose_name = "Role Selection"


