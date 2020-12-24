#!/bin/sh

sudo service mosquitto start
sleep 5
sudo service mosquitto status

# python setup.py install

# Sync DB with the latest migrations.
python manage.py db upgrade

gunicorn -c gunicorn.conf.py wsgi:app
