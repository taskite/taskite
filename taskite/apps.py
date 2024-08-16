from django.apps import AppConfig


class TaskiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "taskite"

    def ready(self):
        import taskite.signals