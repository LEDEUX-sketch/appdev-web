#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser using a small python script for better reliability on Free Plans
if [ "$CREATE_SUPERUSER" = "true" ]; then
  echo "Attempting to create/update superuser..."
  python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
username = '$DJANGO_SUPERUSER_USERNAME'
email = '$DJANGO_SUPERUSER_EMAIL'
password = '$DJANGO_SUPERUSER_PASSWORD'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser "{username}" created successfully.')
else:
    u = User.objects.get(username=username)
    u.set_password(password)
    u.email = email
    u.save()
    print(f'Superuser "{username}" updated successfully.')
END
fi
