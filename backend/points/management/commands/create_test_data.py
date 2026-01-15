"""Команда для создания тестовых данных."""
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point as GeoPoint
from users.models import CustomUser
from points.models import Point, PointMessage

class Command(BaseCommand):
    """Создание тестовых данных."""
    help = "Создание тестовых пользователей и точек"

    def handle(self, *args, **options):
        self.stdout.write("Создание тестовых данных...\n")
        
        user, created = CustomUser.objects.get_or_create(
            username="survivor",
            defaults={
                "display_name": "Выживший",
                "alliance_name": "Пустошные Волки"
            }
        )
        if created:
            user.set_password("wasteland2024")
            user.save()
            self.stdout.write(self.style.SUCCESS(f"✓ Создан пользователь: {user.username}"))  # pylint: disable=no-member
        
        test_points = [
            {
                "title": "Убежище 101",
                "description": "Безопасное место для отдыха",
                "location": GeoPoint(37.618423, 55.751244, srid=4326)
            },
            {
                "title": "Торговый пост",
                "description": "Обмен ресурсами",
                "location": GeoPoint(37.620000, 55.753000, srid=4326)
            },
            {
                "title": "Радиоактивная зона",
                "description": "Опасно! Высокий уровень радиации",
                "location": GeoPoint(37.615000, 55.750000, srid=4326)
            },
        ]
        
        for point_data in test_points:
            point, created = Point.objects.get_or_create(  # pylint: disable=no-member
                title=point_data["title"],
                defaults={
                    "owner": user,
                    "description": point_data["description"],
                    "location": point_data["location"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✓ Создана точка: {point.title}"))  # pylint: disable=no-member
                
                PointMessage.objects.create(  # pylint: disable=no-member
                    point=point,
                    user=user,
                    text=f"Первое сообщение для {point.title}"
                )
        
        self.stdout.write(self.style.SUCCESS("\n✓ Тестовые данные созданы!"))  # pylint: disable=no-member
        self.stdout.write(f"Логин: survivor")
        self.stdout.write(f"Пароль: wasteland2024")
