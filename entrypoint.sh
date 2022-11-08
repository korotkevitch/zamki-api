#!/usr/bin/env sh

python manage.py migrate

python manage.py collectstatic --no-input

exec gunicorn zamki.wsgi:application --bind 0.0.0.0:8000 --reload -w 4