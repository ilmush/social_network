import os

from celery import Celery

from mainapp import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainapp.settings')

app = Celery('mainapp')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()
