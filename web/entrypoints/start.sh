#!/bin/bash

./wait_for_postgres.py

FILE=/code/manage.py
if [ -f "$FILE" ]; then
    echo "Django project has already been started"
else
  django-admin startproject config .
  echo "Django project started"
fi

cp /code/tmp/config/settings.py /code/config/settings.py
cp /code/tmp/config/urls.py /code/config/urls.py
cp /code/tmp/config/logger.py /code/config/logger.py

./manage.py collectstatic --no-input

if [ "$DEV_MODE" == "True" ]; then
  # ./manage.py showmigrations
  ./manage.py makemigrations --no-input
  # By default migrate w/o params apply only on 'default'
  ./manage.py custom_migrate
  # Without faking it, I don't know how to avoid 'another_one' migration
  # being registered on previous default migrate
  # ./manage.py migrate --fake another_one zero
  # ./manage.py migrate another_one --database=switch
  ./manage.py showmigrations
else
  ./manage.py custom_migrate
fi

./manage.py init_admins
./manage.py loaddata data/geocontrib/initial/level_permission.json

gunicorn config.wsgi --bind 0.0.0.0:8080 --workers=3 --access-logfile - --reload --timeout 600
