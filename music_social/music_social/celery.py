import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_social.settings')

celery = Celery('music_social')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
