#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser from env vars (only on first deploy)
if [ "$CREATE_SUPERUSER" = "true" ]; then
  python manage.py createsuperuser --no-input --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" || true
fi
