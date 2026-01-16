> **🗺️Постапокалиптическая система навигации и обмена сообщениями на основе географических координат**

**Wasteland Navigator** - это REST API для работы с географическими точками в постапокалиптическом мире. Система позволяет:

- 📍 Создавать и управлять точками на карте
- 💬 Обмениваться сообщениями с привязкой к локациям
- 🔍 Искать точки и сообщения в заданном радиусе
- 📸 Загружать изображения и файлы
- 👤 Управлять профилями выживших

---

## 🚀 Быстрый старт

### Предварительные требования

- Docker & Docker Compose
- Git

### Установка

1. **Клонируйте репозиторий**
```bash
git clone <repository-url>
cd geo_api
```

2. **Настройте переменные окружения**
```bash
cp .env.example .env
# Отредактируйте .env при необходимости
```

3. **Запустите Docker контейнеры**
```bash
docker-compose up -d --build
```

4. **Примените миграции и инициализируйте проект**
```bash
docker-compose exec web python manage.py migrate
```

5. **Создайте суперпользователя**
```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Создайте тестовые данные (опционально)**
```bash
docker-compose exec web python manage.py create_test_data
```

### Проверка работоспособности

```bash
docker-compose exec web python manage.py check_system

# Health check
curl http://localhost:8000/health/
```

### Доступ к приложению

- 🌐 **Главная страница**: http://localhost:8000/
- 📍 **Список точек**: http://localhost:8000/web/points/
- 💬 **Список сообщений**: http://localhost:8000/web/messages/
- 📚 **Swagger UI**: http://localhost:8000/api/docs/swagger/
- 📖 **ReDoc**: http://localhost:8000/api/docs/redoc/
- 👨‍💼 **Django Admin**: http://localhost:8000/admin/
- 🔍 **Django Silk**: http://localhost:8000/silk/

### 🔐 Авторизация для просмотра карты

Для просмотра точек на карте необходима авторизация:

1. **Получите JWT токен через Swagger UI** (http://localhost:8000/api/docs/swagger/):
   - Откройте раздел `POST /api/auth/login/`
   - Нажмите "Try it out"
   - Используйте тестовые данные:
     ```json
     {
       "username": "survivor",
       "password": "wasteland2024"
     }
     ```
   - Скопируйте значение `access` из ответа

2. **Сохраните токен в браузере**:
   - Откройте http://localhost:8000/
   - Нажмите F12 (откройте консоль разработчика)
   - Перейдите на вкладку Console
   - Выполните команду:
     ```javascript
     localStorage.setItem('access_token', 'ваш_токен_здесь');
     location.reload();
     ```

3. **Готово!** Точки появятся на карте 🗺️

---

## 📚 API Документация

### Авторизация

#### Получение JWT токена
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "survivor",
    "password": "wasteland2024"
  }'
```

**Ответ:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Обновление токена
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

### Регистрация

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "securepass123",
    "password2": "securepass123",
    "display_name": "Странник",
    "alliance_name": "Одиночки"
  }'
```

---

## 🗺️ Примеры запросов

### Получение JWT токена

Сначала получите токен авторизации:

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "survivor",
    "password": "wasteland2024"
  }'
```

**Ответ:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Используйте `access` токен в заголовке `Authorization: Bearer <токен>` для всех последующих запросов.**

---

### 1. Создание точки

```bash
curl -X POST http://localhost:8000/api/points/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Убежище 101",
    "description": "Безопасное место для отдыха",
    "location": {
      "type": "Point",
      "coordinates": [37.618423, 55.751244]
    }
  }'
```

**Ответ:**
```json
{
  "id": 1,
  "title": "Убежище 101",
  "description": "Безопасное место для отдыха",
  "location": {
    "type": "Point",
    "coordinates": [37.618423, 55.751244]
  },
  "owner": 1,
  "owner_display_name": "Выживший",
  "owner_avatar": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### 2. Получение списка точек

```bash
curl -X GET "http://localhost:8000/api/points/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Ответ:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Убежище 101",
      "location": {"type": "Point", "coordinates": [37.618423, 55.751244]},
      "owner_display_name": "Выживший"
    }
  ]
}
```

### 3. Поиск точек в радиусе

```bash
curl -X GET "http://localhost:8000/api/points/search/?latitude=55.751244&longitude=37.618423&radius=5" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Параметры:**
- `latitude` - Широта (обязательно)
- `longitude` - Долгота (обязательно)
- `radius` - Радиус в километрах (обязательно)

### 4. Фильтрация и сортировка точек

```bash
# С пагинацией
curl -X GET "http://localhost:8000/api/points/?page=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# С поиском
curl -X GET "http://localhost:8000/api/points/?search=убежище" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# С сортировкой
curl -X GET "http://localhost:8000/api/points/?ordering=-created_at" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Создание сообщения

```bash
curl -X POST http://localhost:8000/api/messages/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "point=1" \
  -F "text=Здесь безопасно!" \
  -F "image=@photo.jpg"
```

### 6. Поиск сообщений в радиусе

```bash
curl -X GET "http://localhost:8000/api/messages/search_by_radius/?latitude=55.751244&longitude=37.618423&radius=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🧪 Тестирование

### Запуск всех тестов

```bash
docker-compose exec web pytest
```

### Запуск конкретного теста

```bash
docker-compose exec web pytest points/tests/test_views.py
```

### С покрытием кода

```bash
docker-compose exec web pytest --cov=. --cov-report=html
```

### Тестовые данные

После создания тестовых данных доступны:

**Учетные данные:**
- Логин: `survivor`  
- Пароль: `wasteland2024`

**Точки на карте:**
- 5 тестовых точек с координатами в районе Москвы
- Для просмотра на карте требуется авторизация (см. раздел "🔐 Авторизация для просмотра карты")

---

## 📊 Мониторинг

### Health Check

```bash
curl http://localhost:8000/health/
```

**Ответ:**
```json
{
  "status": "healthy",
  "database": "ok",
  "cache": "ok"
}
```

### Django Silk

Профилирование запросов: http://localhost:8000/silk/

### Rollbar

Настройте `ROLLBAR_ACCESS_TOKEN` в `.env` для мониторинга ошибок.

### Логи

```bash
# Просмотр логов
docker-compose logs -f web

# Логи в файле
docker-compose exec web tail -f logs/django.log
```

---

## 📁 Структура проекта

```
geo_api/
├── backend/
│   ├── backend/              # Настройки проекта
│   │   ├── settings/
│   │   │   ├── base.py      # Базовые настройки
│   │   │   ├── local.py     # Dev настройки
│   │   │   └── prod.py      # Production настройки
│   │   ├── urls.py          # URL конфигурация
│   │   └── health.py        # Health check
│   ├── points/              # Приложение точек
│   │   ├── models.py        # Модели Point, PointMessage
│   │   ├── views.py         # API ViewSets
│   │   ├── serializers.py   # DRF сериализаторы
│   │   ├── web_views.py     # HTML views
│   │   ├── tasks.py         # Celery задачи
│   │   ├── tests/           # Тесты
│   │   └── management/      # Management команды
│   ├── users/               # Приложение пользователей
│   │   ├── models.py        # CustomUser модель
│   │   ├── views.py         # API ViewSets
│   │   ├── serializers.py   # Сериализаторы
│   │   └── tasks.py         # Celery задачи
│   ├── templates/           # HTML шаблоны
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── points_list.html
│   │   └── messages_list.html
│   ├── static/              # Статические файлы
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   ├── logs/                # Логи приложения
│   └── manage.py
├── docker-compose.yml       # Docker конфигурация
├── Dockerfile              # Docker образ
├── requirements.txt        # Python зависимости
├── .env.example           # Пример переменных окружения
├── .gitignore             # Git ignore
├── README.md              # Документация
├── CHECKLIST.md           # Чеклист проверки
└── ENV_SETUP.md           # Настройка окружения
```

---

## 🔧 Конфигурация

### Переменные окружения

См. [ENV_SETUP.md](ENV_SETUP.md) для подробной информации.

### Django Settings

- **Development**: `backend.settings.local`
- **Production**: `backend.settings.prod`

### Rate Limiting

- Анонимные: 100 запросов/час
- Авторизованные: 1000 запросов/час

### JWT Токены

- Access token: 1 час
- Refresh token: 7 дней
- Автоматическая ротация включена

---

## 🐛 Troubleshooting

### Проблема: Контейнеры не запускаются

```bash
docker-compose down -v
docker-compose up -d --build
```

### Проблема: Ошибка подключения к БД

```bash
docker-compose exec db psql -U geo_user -d geo_db
```

### Проблема: Celery не работает

```bash
docker-compose logs worker
docker-compose restart worker
```

### Проблема: Статика не загружается

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

## 👨‍💻 Автор

Автор:  Иванов Семен;
Мой Github: https://github.com/IvanovSemjon/;
Мой телефон: +7-999-968-2498;
Моя телега: @ya_ivanov_semjon.

---

**⚠️ WASTELAND NAVIGATOR | СИСТЕМА АКТИВНА ⚠️**
