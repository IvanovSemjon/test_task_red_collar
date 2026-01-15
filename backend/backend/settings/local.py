from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0


INTERNAL_IPS = ["127.0.0.1", "localhost"]

LOGGING["root"]["level"] = "DEBUG"
LOGGING["loggers"]["django.db.backends"]["level"] = "DEBUG"