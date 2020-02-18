#!/bin/bash

./wait_for_postgres.py

if [ "$INSTALL_MODE" == "True" ]; then
  django-admin startproject config .
fi

cp /code/tmp/config/settings.py /code/config/settings.py
cp /code/tmp/config/urls.py /code/config/urls.py
cp /code/tmp/config/logger.py /code/config/logger.py

./manage.py collectstatic --no-input

if [ "$DEV_MODE" == "True" ]; then
  ./manage.py flush --no-input
  ./manage.py showmigrations
  ./manage.py makemigrations --no-input
  ./manage.py migrate
  ./manage.py showmigrations
  # ./manage.py init_admins
  # ./manage.py init_fixtures
else
  ./manage.py migrate
fi

gunicorn config.wsgi --bind 0.0.0.0:8080 --workers=3 --access-logfile - --reload --timeout 600
