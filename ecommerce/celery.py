import os
from celery import Celery
from celery import shared_task


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

app = Celery('ecommerce')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# мониторинг износа колеса
@shared_task(name="repeat_sync_google_sheet", queue='local')
def sync_google_sheet():
    pass

# app.conf.beat_schedule = {
#     'sync_google_sheet': {
#         'task': 'repeat_sync_google_sheet',
#         'schedule': datetime.timedelta(seconds=60),
#     },
# }
