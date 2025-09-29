#!/bin/sh
set -e  # Para abortar se qualquer comando falhar

echo "=== Rodando migrations do Django ==="
# Substitua "webhooks" pelo nome do app do seu modelo ManifestoWebhook
python manage.py makemigrations webhooks
python manage.py migrate

echo "=== Iniciando Gunicorn ==="
exec gunicorn core.wsgi:application --bind 0.0.0.0:5000 --workers 3 --timeout 120
