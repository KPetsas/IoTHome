#!/bin/sh

sudo service mosquitto start
sleep 5
cd api/
gunicorn -c gunicorn.conf.py wsgi:app
