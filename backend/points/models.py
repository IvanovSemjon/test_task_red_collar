"""Модель точки с географическими координатами."""
from django.contrib.gis.db import models
from django.conf import settings

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
