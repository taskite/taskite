from django.apps import AppConfig


class CalyvimConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calyvim"

    def ready(self):
        import calyvim.signals