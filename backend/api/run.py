"""
Entry point of the application.
"""

from api import constants
from api.initialization import create_app


# Call the application factory function to construct a Flask application instance using the configuration.
app = create_app(__name__, constants.FLASK_CONFIGURATION_FILE)
