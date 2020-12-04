"""
This is a command line utility. Use it to manage migrations,
create the tables in DB, or start the development server.
"""

import os
import pkgutil
import importlib

import constants

from flask_script import Manager
from flask_migrate import MigrateCommand

from initialization import create_app


# Import all models to create the related tables.
# Application convention: Every application model is set in a models.py module under its related package.
for loader, module_name, ispkg in pkgutil.iter_modules(path=[os.getcwd()]):
    if ispkg:
        try:
            importlib.import_module('.models', package=module_name)
        except ImportError:
            continue

manager = Manager(create_app(__name__, constants.FLASK_CONFIGURATION_FILE))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
