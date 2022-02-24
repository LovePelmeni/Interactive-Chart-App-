#!/bin/sh

if [ "$DATABASE" == "postgres"]
then
  echo 'Waiting for POSTGRES....'
  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo 'POSTGRES started....'

fi

python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"