import os
from taskite.settings.base import *

CSRF_TRUSTED_ORIGINS = ["http://localhost:5173"]
DEBUG = True
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
APP_URL = os.environ.get("APP_URL", "http://localhost:5173")

CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "redis://localhost:6379/1")

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "<Taskite no-reply@taskite.in>"
)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = "1025"

DJANGO_VITE = {
  "default": {
    "dev_mode": True
  }
}

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
