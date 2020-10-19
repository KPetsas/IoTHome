"""
Entry point of the application.
"""

import os
import pkgutil
import importlib

from app_initialization import app, api
from mqtt_initialization import MQTT
from router import Router


# Initialize MQTT.
mqtt = MQTT(app)

# Application convention: Every application route is set in a routes.py module under its related package.
for loader, module_name, ispkg in pkgutil.iter_modules(path=[os.getcwd()]):
    if ispkg:
        importlib.import_module('.routes', package=module_name)

# Register all application routes automatically.
for route in Router.__subclasses__():
    route(api)
