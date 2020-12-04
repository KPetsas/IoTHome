import logging

import configuration.settings as config
import constants


class Logger():
    def init_app(self, app):
        """ Logger setup. """
        # Logger settings.
        log_format = constants.LOG_FORMAT
        date_format = constants.LOG_DATE_FORMAT
        log_level = logging.DEBUG if eval(config.LOG_DEBUG) else logging.INFO
        # Set root logger.
        logging.basicConfig(format=log_format, level=log_level, datefmt=date_format)

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
