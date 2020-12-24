import logging

from api.configuration import settings as config
from api import constants


class Logger():
    def init_app(self, app):
        """ Logger setup. """
        # Logger settings.
        log_format = constants.LOG_FORMAT
        date_format = constants.LOG_DATE_FORMAT
        log_level = logging.DEBUG if config.LOG_DEBUG else logging.INFO
        # Set root logger.
        logging.basicConfig(format=log_format, level=log_level, datefmt=date_format)

        if config.PRODUCTION:
            # Configure Flask to output its logs with Gunicorn handlers.
            gunicorn_error_logger = logging.getLogger('gunicorn.error')
            app.logger.handlers.extend(gunicorn_error_logger.handlers)

            gunicorn_access_logger = logging.getLogger('gunicorn.access')
            app.logger.handlers.extend(gunicorn_access_logger.handlers)

            # Set the logging level of Gunicorn to the same as Flask.
            # app.logger.setLevel(gunicorn_logger.level)
            app.logger.setLevel(log_level)
            app.logger.info("Gunicorn logger set.")

        self._logger = app.logger

    @property
    def info(self):
        """ Info level getter. """
        return self._logger.info

    @property
    def warn(self):
        """ Warning level getter. """
        return self._logger.warn

    @property
    def error(self):
        """ Error level getter. """
        return self._logger.error

    @property
    def debug(self):
        """ Debug level getter. """
        return self._logger.debug
