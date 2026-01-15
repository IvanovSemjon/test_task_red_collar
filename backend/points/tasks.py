from celery import shared_task  # pylint: disable=no-name-in-module
from PIL import Image
from django.core.files.base import ContentFile
from django.conf import settings
import io
import rollbar  # pylint: disable=import-error
from .models import PointMessage

ROLLBAR_ACCESS_TOKEN = getattr(settings, "ROLLBAR_ACCESS_TOKEN", None)

@shared_task(bind=True)
def generate_message_image_thumbnail(self, message_id, size=(200, 200)):
    try:
        msg = PointMessage.objects.get(id=message_id)  # pylint: disable=no-member
        if not msg.image:
            return

        img = Image.open(msg.image)
        img.thumbnail(size)

        thumb_io = io.BytesIO()
        img.save(thumb_io, img.format)
        msg.image.save(f"thumb_{msg.image.name}", ContentFile(thumb_io.getvalue()), save=True)
    except Exception as e:
        if ROLLBAR_ACCESS_TOKEN:
            rollbar.report_exc_info()
        raise e
