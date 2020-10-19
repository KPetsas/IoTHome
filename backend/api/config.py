"""
The configuration of the application.
"""

import os

# Environment variables
PRODUCTION = os.environ.get("PRODUCTION", False)
CACHE_ENABLED = os.environ.get("CACHE_ENABLED", False)

MQTT_IP = os.environ.get("MQTT_IP")
MQTT_PORT = int(os.environ.get("MQTT_PORT"))
CA_CERT_PATH = os.environ.get("CA_CERT_PATH")

WIFI_SSID_PASS = os.environ.get("WIFI_SSID_PASS")
LOG_DEBUG = os.environ.get("LOG_DEBUG").capitalize()

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
SECRET_KEY = os.environ.get("SECRET_KEY")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

SWAGGER_ENABLED = os.environ.get("SWAGGER_ENABLED", not PRODUCTION)
