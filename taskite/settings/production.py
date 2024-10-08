import os
import sentry_sdk
import dj_database_url
from taskite.settings.base import *

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
CSRF_TRUSTED_ORIGINS = ["https://app.taskite.in"]

BASE_URL = os.environ.get("BASE_URL", "https://app.taskite.in")

CELERY_BROKER_URL = os.environ.get("REDIS_URL")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")


DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}

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

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
    }
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

DJANGO_VITE = {
  "default": {
    "dev_mode": False,
    "static_url_prefix": "dist",
    "manifest_path": BASE_DIR / "taskite" / "static" / "dist" / "manifest.json"
  }
}

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
          "bucket_name": AWS_STORAGE_BUCKET_NAME,
          "region_name": AWS_S3_REGION_NAME,
          "access_key": AWS_ACCESS_KEY_ID,
          "secret_key": AWS_SECRET_ACCESS_KEY,
          "querystring_auth": False
        },
    },
}

USE_S3 = True