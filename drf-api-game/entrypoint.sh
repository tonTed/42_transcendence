#!/bin/sh

cd src
python manage.py makemigrations
python manage.py migrate

exec python manage.py runserver 0.0.0.0:3002