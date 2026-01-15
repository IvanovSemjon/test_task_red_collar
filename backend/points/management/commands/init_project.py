"""Команда для инициализации проекта."""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    """Инициализация проекта после первого запуска."""
    help = "Инициализация проекта (создание Site и т.д.)"

    def handle(self, *args, **options):
        self.stdout.write("Инициализация проекта...\n")
        
        # Создаем Site
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': 'localhost:8000',
                'name': 'Wasteland Navigator'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Создан Site: {site.name}"))  # pylint: disable=no-member
        else:
            self.stdout.write(self.style.WARNING(f"Site уже существует: {site.name}"))  # pylint: disable=no-member
        
        self.stdout.write(self.style.SUCCESS("\n✓ Инициализация завершена!"))  # pylint: disable=no-member
        self.stdout.write("Теперь можно создать суперпользователя:")
        self.stdout.write("  docker-compose exec web python manage.py createsuperuser")
