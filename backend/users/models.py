"""Определение класса пользователя."""
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True
    )

    # Даем возможность обозначить себя и написать имя или "погоняло"
    # Мы же все таки в диком постметеоритном мире, хаос и анархия.
    display_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Ваш позывной"
    )

    # Люди как всегда социальны и сбиваются в группы и банды для выживания
    # А у каждой уважающей себя банды есть название гремящее на все пустоши.
    alliance_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Название сообщества"
    )

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
        help_text="Группы пользователя"
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",
        blank=True,
        help_text="Разрешения пользователя"
    )

    def __str__(self):
        """
        Показывать display_name или username"""
        return self.display_name or self.username
    





