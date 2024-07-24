#!/bin/sh

cd src

sleep 5

python manage.py makemigrations
python manage.py migrate

python mock/seed_users.py
exec python manage.py runserver 0.0.0.0:3001