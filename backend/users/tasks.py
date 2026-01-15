from celery import shared_task  # pylint: disable=no-name-in-module
from PIL import Image
from django.core.files.base import ContentFile
import io
from .models import CustomUser
import rollbar  # pylint: disable=import-error
from django.conf import settings

ROLLBAR_ACCESS_TOKEN = getattr(settings, "ROLLBAR_ACCESS_TOKEN", None)

@shared_task(bind=True)
def generate_avatar_thumbnail(self, user_id, size=(100, 100)):
    try:
        user = CustomUser.objects.get(id=user_id)
        if not user.avatar:
            return

        img = Image.open(user.avatar)
        img.thumbnail(size)

        thumb_io = io.BytesIO()
        img.save(thumb_io, img.format)
        user.avatar.save(f"thumb_{user.avatar.name}", ContentFile(thumb_io.getvalue()), save=True)
    except Exception as e:
        if ROLLBAR_ACCESS_TOKEN:
            rollbar.report_exc_info()
        raise e