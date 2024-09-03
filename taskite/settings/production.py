import os
from taskite.settings.base import *

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

BASE_URL = os.environ.get("BASE_URL", "https://taskite.in")
APP_URL = os.environ.get("APP_URL", "https://taskite.in")

CELERY_BROKER_URL = os.environ.get("REDIS_URL")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "<Taskite no-reply@taskite.in>"
)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USERNAME = os.environ.get("EMAIL_HOST_USERNAME")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Scout settings
SCOUT_MONITOR = True
SCOUT_KEY = os.environ.get("SCOUT_KEY")
SCOUT_NAME = os.environ.get("SCOUT_NAME", "Taskite")