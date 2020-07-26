from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from datetime import timedelta

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectNotifyv2_be.settings')

app = Celery('projectNotifyv2_be')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
