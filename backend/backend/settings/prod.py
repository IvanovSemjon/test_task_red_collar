from .base import *

DEBUG = False

# Безопасность для production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Логирование только ошибок
LOGGING["root"]["level"] = "ERROR"
LOGGING["loggers"]["django"]["level"] = "ERROR"

# Отключаем Browsable API
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
]

# Усиленный throttling
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "anon": "50/hour",
    "user": "500/hour",
}