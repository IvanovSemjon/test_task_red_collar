from celery import shared_task  # pylint: disable=no-name-in-module

from PIL import Image
from django.core.files.base import ContentFile
import io
from .models import CustomUser

@shared_task
def generate_avatar_thumbnail(user_id, size=(100, 100)):
    user = CustomUser.objects.get(id=user_id)
    if not user.avatar:
        return

    img = Image.open(user.avatar)
    img.thumbnail(size)

    thumb_io = io.BytesIO()
    img.save(thumb_io, img.format)
    user.avatar.save(f"thumb_{user.avatar.name}", ContentFile(thumb_io.getvalue()), save=True)