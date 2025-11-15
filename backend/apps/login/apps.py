from django.apps import AppConfig

class LoginConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "apps.login"
    verbose_name = "Login Module"