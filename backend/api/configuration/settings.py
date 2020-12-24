"""
The configuration of the application.
"""

import os

from pathlib import Path


# Environment variables
PRODUCTION = os.environ.get("PRODUCTION", "False").capitalize() == "True"
CACHE_ENABLED = os.environ.get("CACHE_ENABLED", "False").capitalize() == "True"

MQTT_IP = os.environ.get("MQTT_IP")
_DEFAULT_MQTT_PORT = 1883
_MQTT_PORT_ENV = os.environ.get("MQTT_PORT")
MQTT_PORT = int(_MQTT_PORT_ENV) if _MQTT_PORT_ENV else _DEFAULT_MQTT_PORT
CA_CERT_PATH = os.environ.get("CA_CERT_PATH")

WIFI_SSID_PASS = os.environ.get("WIFI_SSID_PASS")

LOG_DEBUG = os.environ.get("LOG_DEBUG", "False").capitalize() == "True"

# Directory to keep data related to the application, such as the sqlite db.
USER_CONFIG_PATH = "{0}/.config/smart_home".format(Path.home())
# Create the directory if it does not exist (~/.config/smart_home/)
Path(USER_CONFIG_PATH).mkdir(parents=True, exist_ok=True)

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SQLALCHEMY_DATABASE_URI", "sqlite:///{0}/app.db".format(USER_CONFIG_PATH))

SECRET_KEY = os.environ.get("SECRET_KEY")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

TIMEZONE = os.environ.get("TIMEZONE", 'Europe/Athens')

SWAGGER_ENABLED = os.environ.get("SWAGGER_ENABLED", not PRODUCTION)
