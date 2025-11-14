from django.apps import AppConfig


class ForgetPasswordConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "apps.forgetpassword"
    verbose_name = "Password Recovery"


