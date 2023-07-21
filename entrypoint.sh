#!/bin/bash

python manage.py collectstatic --no-input --clear

# gunicorn -w 2 -b 0.0.0.0:8000 code/core.wsgi:application

exec "$@"