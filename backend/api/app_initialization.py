"""
Initialization of the application.
"""

import logging

import config

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from devices.cache import DevicesCache


app = Flask(__name__)

# Logger settings.
log_format = "%(asctime)s %(levelname)s: %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"
log_level = logging.DEBUG if eval(config.LOG_DEBUG) else logging.INFO
# Set root logger.
logging.basicConfig(format=log_format, level=log_level, datefmt=date_format)

# Error handling works properly when using flask-restful, if only we set the following configuration.
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.SECRET_KEY

app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY

app.config['JWT_BLACKLIST_ENABLED'] = False
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.config['SESSION_COOKIE_HTTPONLY'] = True


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

# Register blueprint.
app.register_blueprint(api_blueprint, url_prefix='/api')


CORS(app)

jwt = JWTManager(app)
db = SQLAlchemy(app)


# Initialize cache.
devices_cache = DevicesCache(app) if config.CACHE_ENABLED else None


@app.before_first_request
def create_tables():
    db.create_all()
