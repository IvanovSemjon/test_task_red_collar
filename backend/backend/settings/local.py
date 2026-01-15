from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Отключаем HTTPS для разработки
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0

# Дополнительные настройки для разработки
INTERNAL_IPS = ["127.0.0.1", "localhost"]

# Более подробное логирование
LOGGING["root"]["level"] = "DEBUG"
LOGGING["loggers"]["django.db.backends"]["level"] = "DEBUG"