"""Определение класса пользователя."""
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    """
    Кастомный класс пользователя.
    """
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True
    )

    # Даем возможность обозначить себя и написать имя или "погоняло"
    # Мы же все таки в диком постметеоритном мире и вокруг хаос и анархия.
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
        help_text="Название группировки"
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

    def __str__(self) -> str:
        """
        Показывать display_name или username"""
        return str(self.display_name or self.username)
    



@receiver(post_save, sender=CustomUser)
def post_avatar_save(sender, instance, created, **kwargs):
    if instance.avatar:
        from .tasks import generate_avatar_thumbnail
        generate_avatar_thumbnail.delay(instance.id)
