"""Команда для проверки системы."""
from django.core.management.base import BaseCommand
from django.db import connection
from django.core.cache import cache
from django.conf import settings

class Command(BaseCommand):
    """Проверка всех компонентов системы."""
    help = "Проверка работоспособности всех компонентов"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=== ПРОВЕРКА СИСТЕМЫ ===\n"))  # pylint: disable=no-member
        
        self.stdout.write("Проверка базы данных...")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version()")
                version = cursor.fetchone()[0]
            self.stdout.write(self.style.SUCCESS(f"✓ БД работает: {version}\n"))  # pylint: disable=no-member
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Ошибка БД: {e}\n"))  # pylint: disable=no-member
        
        self.stdout.write("Проверка Redis кэша...")
        try:
            cache.set("test_key", "test_value", 10)
            value = cache.get("test_key")
            if value == "test_value":
                self.stdout.write(self.style.SUCCESS("✓ Redis работает\n"))  # pylint: disable=no-member
            else:
                self.stdout.write(self.style.ERROR("✗ Redis не работает\n"))  # pylint: disable=no-member
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Ошибка Redis: {e}\n"))  # pylint: disable=no-member
        
        self.stdout.write("Проверка настроек...")
        self.stdout.write(f"DEBUG: {settings.DEBUG}")
        self.stdout.write(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        self.stdout.write(f"SECRET_KEY установлен: {'Да' if settings.SECRET_KEY else 'Нет'}")
        
        self.stdout.write(self.style.SUCCESS("\n=== ПРОВЕРКА ЗАВЕРШЕНА ==="))  # pylint: disable=no-member
