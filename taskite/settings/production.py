from taskite.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['taskite-7a7818f32166.herokuapp.com']

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

