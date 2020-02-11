#!/bin/bash

./wait_for_postgres.py

./manage.py collectstatic --no-input

if [ "$DEV_MODE" == "True" ]; then
  ./manage.py showmigrations
  ./manage.py makemigrations --no-input
  ./manage.py migrate
  ./manage.py showmigrations
  ./manage.py init_admins
  ./manage.py init_fixtures
else
  ./manage.py migrate
fi

gunicorn config.wsgi --bind 0.0.0.0:8080 --workers=3 --access-logfile - --reload --timeout 600
