from dotenv import load_dotenv
import dj_database_url
load_dotenv()  # take environment variables from .env.

from taskite.settings.base import *

CSRF_TRUSTED_ORIGINS = ["http://localhost:5173"]
DEBUG = True
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "redis://localhost:6379/1")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = "1025"

DJANGO_VITE = {
  "default": {
    "dev_mode": True
  }
}

USE_S3 = False

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")

DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}

if USE_S3:
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
            "querystring_auth": False,
            "location": "uploads"
          },
      },
  }

# CORS_ALLOW_ALL_ORIGINS = True

# LOGGING = {
#     'version': 1,
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         }
#     }
# }
