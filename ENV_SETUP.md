# Настройка переменных окружения

## Быстрый старт

1. Скопируйте файл `.env.example` в `.env`:
```bash
cp .env.example .env
```

2. Отредактируйте `.env` файл с вашими настройками

## Описание переменных

### Django Settings
- `DEBUG` - Режим отладки (1 для dev, 0 для prod)
- `SECRET_KEY` - Секретный ключ Django (сгенерируйте новый для production!)
- `DJANGO_SETTINGS_MODULE` - Модуль настроек (backend.settings.local или backend.settings.prod)

### Database
- `POSTGRES_DB` - Имя базы данных
- `POSTGRES_USER` - Пользователь БД
- `POSTGRES_PASSWORD` - Пароль БД
- `POSTGRES_HOST` - Хост БД (обычно 'db' в Docker)
- `POSTGRES_PORT` - Порт БД (обычно 5432)

### Redis & Celery
- `CELERY_BROKER_URL` - URL брокера Celery
- `CELERY_RESULT_BACKEND` - URL для результатов Celery

### Monitoring (опционально)
- `ROLLBAR_ACCESS_TOKEN` - Токен Rollbar для мониторинга ошибок
- `SENTRY_DSN` - DSN Sentry для мониторинга
- `ENVIRONMENT` - Окружение (development/staging/production)

## Генерация SECRET_KEY

Для production сгенерируйте новый SECRET_KEY:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Важно!

⚠️ **НИКОГДА не коммитьте файл `.env` в git!**
⚠️ **Используйте разные SECRET_KEY для dev и production!**
⚠️ **Меняйте пароли БД в production!**
