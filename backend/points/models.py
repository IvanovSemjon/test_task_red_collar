"""Модель точки с географическими координатами."""
from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()

class Point(models.Model):
    """
    Класс точка с географическими координатами.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="points",
        verbose_name="Владелец точки"
    )
    title = models.CharField(max_length=100, verbose_name="Название точки")
    description = models.TextField(blank=True, null=True, verbose_name="Описание точки")
    location = models.PointField(srid=4326, verbose_name="Координаты")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        """
        Мета информация о модели точки.
        """
        verbose_name = "Точка"
        verbose_name_plural = "Точки"
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]

    def __str__(self):
        """
        Строковое представление модели точки.
        """
        return f"{self.title} ({self.owner})"


class PointMessage(models.Model):
    """
    Возможность добавления сообщений к точке.
    """
    point = models.ForeignKey("Point", on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    file = models.FileField(upload_to="point_messages_files/", null=True, blank=True)
    image = models.ImageField(upload_to="point_messages_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Message by {self.user.username} on {self.point.title}"  # pylint: disable=no-member
