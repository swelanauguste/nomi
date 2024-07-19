#!/bin/sh

# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi

# python manage.py migrate
python manage.py makemigrations
python manage.py migrate
# python manage.py createsuperuser --username kingship --email kingship.lc@gmail.com --noinput
# python manage.py loaddata  --exclude=auth.permission --exclude=contenttypes db3_5_2024.json
# python manage.py collectstatic --noinput

exec "$@"