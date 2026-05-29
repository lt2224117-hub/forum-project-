#!/bin/bash
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth.models import User
u = User.objects.filter(username='Admin').first()
if u:
    u.is_staff = True
    u.is_superuser = True
    u.set_password('Admin123456')
    u.save()
    print('Done')
"
gunicorn config.wsgi:application --bind 0.0.0.0:8000