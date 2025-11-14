from django.apps import AppConfig

class HomeConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = 'backend.apps.home'
    verbose_name = "Home (Landing)"