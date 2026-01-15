import os
from celery import Celery
from celery.signals import task_failure  # pylint: disable=import-error,no-name-in-module
import rollbar  # pylint: disable=import-error
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.base")

app = Celery("backend")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

ROLLBAR_ACCESS_TOKEN = getattr(settings, "ROLLBAR_ACCESS_TOKEN", None)
ENVIRONMENT = getattr(settings, "ENVIRONMENT", "development")

if ROLLBAR_ACCESS_TOKEN:
    rollbar.init(
        access_token=ROLLBAR_ACCESS_TOKEN,
        environment=ENVIRONMENT,
        root=str(settings.BASE_DIR),
    )

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, args=None, kwargs=None, traceback=None, einfo=None, **kw):
    if ROLLBAR_ACCESS_TOKEN:
        rollbar.report_exc_info((type(exception), exception, traceback))