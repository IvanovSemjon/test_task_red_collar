from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("POSTGRES_DB", "geo_db"),
        "USER": os.getenv("POSTGRES_USER", "geo_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "geo_pass"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
    }
}

ALLOWED_HOSTS = ["*"]