import os
from calyvim.settings.base import *
import dj_database_url
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

CSRF_TRUSTED_ORIGINS = ["http://localhost:3085"]
DEBUG = True
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8085")
APP_URL = os.environ.get("APP_URL", "http://localhost:3085")
DJANGO_ALLOW_ASYNC_UNSAFE = True

CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "redis://localhost:6379/1")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = "1025"

# DJANGO_VITE = {
#     "default": {
#         "dev_mode": False,
#         "static_url_prefix": "dist",
#         "manifest_path": BASE_DIR / "calyvim" / "static" / "dist" / "manifest.json",
#     }
# }

DJANGO_VITE = {
  "default": {
    "dev_mode": True,
    "dev_server_port": "3085"
  }
}

DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://calyvim:calyvim@localhost:5432/calyvim"
    ),
    "test": dj_database_url.config(
        default="postgresql://calyvim:calyvim@localhost:5432/calyvim_testing"
    ),
}
