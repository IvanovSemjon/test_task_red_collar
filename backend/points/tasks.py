from celery import shared_task  # pylint: disable=no-name-in-module

from PIL import Image
from django.core.files.base import ContentFile
import io
from .models import PointMessage

@shared_task
def generate_message_image_thumbnail(message_id, size=(200, 200)):
    msg = PointMessage.objects.get(id=message_id)  # pylint: disable=no-member
    if not msg.image:
        return

    img = Image.open(msg.image)
    img.thumbnail(size)

    thumb_io = io.BytesIO()
    img.save(thumb_io, img.format)
    msg.image.save(f"thumb_{msg.image.name}", ContentFile(thumb_io.getvalue()), save=True)