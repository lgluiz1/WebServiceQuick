from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Define o settings do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Carrega configurações do Django com prefixo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre tasks automaticamente
app.autodiscover_tasks()

# Scheduler do Django-Celery-Beat
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

# Configurações adicionais importantes
app.conf.update(
    broker_url='amqp://guest:guest@rabbitmq:5672//',  # conexão com RabbitMQ
    result_backend='django-db',                         # backend de resultados
    task_acks_late=True,                                # ack só depois de executar a task
    task_default_queue='celery',
    task_queues={
        'celery': {
            'exchange': 'celery',
            'routing_key': 'celery',
            'durable': True,                           # garante que messages não se percam
        },
    },
    timezone='America/Sao_Paulo',
    enable_utc=False,
)
