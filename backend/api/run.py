"""
Entry point of the application.
"""

import constants

from initialization import create_app


# Call the application factory function to construct a Flask application instance using the configuration.
app = create_app(__name__, constants.FLASK_CONFIGURATION_FILE)
