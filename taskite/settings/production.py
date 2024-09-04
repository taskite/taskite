import os
import sentry_sdk
import dj_database_url
from taskite.settings.base import *

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
CSRF_TRUSTED_ORIGINS = ["https://taskite.in"]

BASE_URL = os.environ.get("BASE_URL", "https://taskite.in")
APP_URL = os.environ.get("APP_URL", "https://taskite.in")

CELERY_BROKER_URL = os.environ.get("REDIS_URL")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")


DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "<Taskite no-reply@taskite.in>"
)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
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


# Sentry Setup
sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
)
