#!/bin/sh

echo "⏳ Waiting for Postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done

echo "✅ Postgres is up"

echo "🧱 Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "🚀 Starting Django server..."
exec "$@"