from __future__ import absolute_import, unicode_literals  # deve ser a primeira linha

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# Use Django Scheduler (Beat)
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'