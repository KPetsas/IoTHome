"""
Gunicorn wsgi application server configuration for production deployment.
"""

chdir = "/usr/src/app"

bind = "0.0.0.0:9191"

user = None
group = None

# Bottleneck!
# One worker due to flask-mqtt limitation -> More info: https://flask-mqtt.readthedocs.io/en/latest/#limitations
workers = 1
timeout = 90
worker_class = "sync"

daemon = False

access_logfile = "/tmp/gunicorn_access.log"
error_logfile = "/tmp/gunicorn_error.log"
