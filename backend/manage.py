"""
This is a command line utility. Use it to manage migrations,
create the tables in DB, or start the development server.
"""

import pkgutil
import importlib

from flask_script import Manager
from flask_migrate import MigrateCommand

from api import constants
from api.initialization import create_app


manager = Manager(create_app(__name__, constants.FLASK_CONFIGURATION_FILE))

# Import all models to create the related tables.
# Application convention: Every application model is set in a models.py module under its related package.
for loader, module_name, ispkg in pkgutil.iter_modules(path=[constants.APPLICATION_DIR]):
    if ispkg:
        try:
            importlib.import_module('.models', package='api.' + module_name)
        except ImportError:
            continue

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
