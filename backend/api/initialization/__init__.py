"""
Initialization of the application.
"""

import os
import pkgutil
import importlib

import configuration.settings as config
import constants

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from initialization.logger_initialization import Logger
from initialization.scheduler_initialization import Scheduler
from initialization.mqtt_initialization import MQTT
from router import Router
from devices.cache import DevicesCache


# Create the instances of the Flask extensions in the global scope.
logger = Logger()
api = Api()
jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()
scheduler = Scheduler()
mqtt = MQTT()

devices_cache = DevicesCache() if config.CACHE_ENABLED else None

if config.SWAGGER_ENABLED:
    swagger = Swagger()


def register_app_routes(create_app_func):
    """
    Decorator to ensure that all routes will be registered
    after the application instantiation, initialization and setup completes.
    Also, ensures to register the API Blueprints after the routes registration.
    """

    def application_factory(main_module_name, config_file=None):
        """ Create an application instance and register all routes. """
        app = create_app_func(main_module_name, config_file)

        # Application convention: Every application route is set in a routes.py module under its related package.
        for loader, module_name, ispkg in pkgutil.iter_modules(path=[os.getcwd()]):
            if ispkg:
                try:
                    importlib.import_module('.routes', package=module_name)
                except ImportError:
                    continue

        # Register all application routes automatically.
        for route in Router.__subclasses__():
            route(api)

        # Initialize Api and register blueprint after the routes registration.
        api_blueprint = Blueprint('api', main_module_name)
        api.init_app(api_blueprint)
        app.register_blueprint(api_blueprint, url_prefix='/api')

        return app
    return application_factory


@register_app_routes
def create_app(main_module_name, config_file):
    """ Application Factory Function. """
    app = Flask(main_module_name)

    if config_file:
        config_file = os.path.join(app.root_path,
                                   constants.CONFIGURATION_DIR, config_file)
        app.config.from_pyfile(config_file)

    initialize_extensions_and_db(app)
    return app


def initialize_extensions_and_db(app):
    """ Bind every extension instance, with the Flask app application instance. """
    logger.init_app(app)

    CORS(app)
    jwt.init_app(app)

    # DB initialization.
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)

    # Initialize Advanced Python Scheduler (after DB initialization).
    scheduler.init_app(app)

    # Initialize MQTT.
    mqtt.init_app(app)

    if config.CACHE_ENABLED:
        # Initialize cache.
        devices_cache.init_app(app)

    if config.SWAGGER_ENABLED:
        swagger.init_app(app)
