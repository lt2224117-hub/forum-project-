#!/usr/bin/env bash
# v2
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --noinput || true
python manage.py shell -c "
from django.contrib.auth.models import User
u = User.objects.filter(username='Admin').first()
if u:
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print('Done')
"