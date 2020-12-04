#!/bin/sh

sudo service mosquitto start
sleep 5
cd api/

# Sync DB with the latest migrations.
python manage.py db upgrade

gunicorn -c gunicorn.conf.py wsgi:app
