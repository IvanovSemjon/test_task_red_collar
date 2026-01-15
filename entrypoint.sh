#!/bin/sh

echo "⏳ Waiting for Postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done

echo "✅ Postgres is up"

echo "🧱 Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

if [ -z "$DJANGO_SUPERUSER_USERNAME" ]; then
  echo "⚠️  DJANGO_SUPERUSER_USERNAME not set, skipping superuser creation"
else
  echo "👑 Creating superuser if not exists..."
  python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')"
fi

echo "🚀 Starting Django server..."
exec "$@"