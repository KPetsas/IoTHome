import time

import config
import constants

from datetime import datetime

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from run import mqtt, scheduler
from app_initialization import app, devices_cache
from auth.models import UserModel
from devices.models import DeviceModel


# EXAMPLE URL: http://192.168.1.50:9191/api/wifi_switches
class WifiSwitchAction(Resource):
    """ Control every wifi switch through this controller. """

    def __init__(self):
        """ Setup the request arguments parser in the constructor. """

        # Associate the trigger with the related function.
        self._trigger_scheduler = {'date': self._date_scheduler,
                                   'cron': self._cron_scheduler, 'interval': self._interval_scheduler}

        self._parser = reqparse.RequestParser()
        self._parser.add_argument('device_ui_id', help='This field cannot be blank', required=True)
        self._parser.add_argument('action', help='This field cannot be blank', required=False)
        self._parser.add_argument('trigger', choices=('date', 'interval', 'cron'),
                                  help='trigger must be: date, interval or cron', required=False)
        self._parser.add_argument('datetime',
                                  help='Comma separated values: {0}'.format(constants.DATETIME_CSV), required=False)
        self._parser.add_argument(
            'week', help='In case of trigger interval and cron you can specify the week.', required=False)
        self._parser.add_argument(
            'day_of_week', help='In case of trigger cron you can specify the day of the week.', required=False)
        self._parser.add_argument(
            'start_date', help='In case of trigger interval and cron you can specify the start date.', required=False)
        self._parser.add_argument(
            'end_date', help='In case of trigger interval and cron you can specify the end date.', required=False)

    @jwt_required
    @swag_from('swagger/wifi_switch_action_swag.yml')
    def put(self):
        """ PUT request that requires JWT to update device. """

        app.logger.debug("Resource WifiSwitchAction to update device with PUT.")

        # Retrieve the username from the JWT and find the current user from DB.
        current_user = UserModel.find_by_username(get_jwt_identity())

        # Parse request arguments.
        args = self._parser.parse_args()
        device_ui_id = args.get('device_ui_id')
        action = args.get('action')

        # Handle on/off actions.
        return self._device_switch_util(current_user.id, device_ui_id, action)

    @jwt_required
    @swag_from('swagger/wifi_switch_timer_swag.yml')
    def post(self):
        """ POST request that requires JWT to schedule timer or set specific time to change the state of a device. """

        app.logger.info("Resource WifiSwitchAction to set timer for device with POST.")

        # Retrieve the username from the JWT and find the current user from DB.
        current_user = UserModel.find_by_username(get_jwt_identity())

        # Parse request arguments.
        request_args = self._parser.parse_args()

        # Update the dictionary (like 'year': 2020) and get the keys from DATETIME_CSV tuple. Convert empty strings to None and splitted datetime strings to integers.
        request_args.update(dict(zip(constants.DATETIME_CSV, map(
            lambda d: None if not d else int(d), request_args.get('datetime').split(',')))))

        # Call the scheduler function related to the trigger.
        self._trigger_scheduler[request_args.get('trigger')](current_user.id, request_args)

        return (dict(message='Job scheduled.'), 200)

    @jwt_required
    @swag_from('swagger/wifi_switch_remove_timer_swag.yml')
    def delete(self):
        """ Remove a scheduled job. """
        # Parse request arguments.
        args = self._parser.parse_args()

        # Remove the scheduled job.
        scheduler.remove_job(args.get('device_ui_id'))

    @classmethod
    def _date_scheduler(cls, user_id, request_args):
        """
        Schedule a job to run at a specific date and time.

        :param (int) user_id: The user ID.
        :param (dict) request_args: The request arguments.
        """
        scheduler.add_job(cls._device_switch_util, args=(user_id, request_args.get('device_ui_id'), request_args.get('action')),
                          trigger=request_args.get('trigger'),
                          run_date=datetime(request_args.get('year'), request_args.get('month'), request_args.get('day'),
                                            request_args.get('hours'), request_args.get('minutes'), request_args.get('seconds')),
                          id=request_args.get('device_ui_id'), replace_existing=True)

    @classmethod
    def _interval_scheduler(cls, user_id, request_args):
        """
        Schedule a job to run at every specified interval.

        :param (int) user_id: The user ID.
        :param (dict) request_args: The request arguments.
        """
        scheduler.add_job(cls._device_switch_util, args=(user_id, request_args.get('device_ui_id'), request_args.get('action')),
                          trigger=request_args.get('trigger'), weeks=request_args.get('week') or 0, days=request_args.get('day') or 0,
                          hours=request_args.get('hours') or 0, minutes=request_args.get('minutes') or 0, seconds=request_args.get('seconds') or 0,
                          start_date=request_args.get('start_date'), end_date=request_args.get('end_date'), id=request_args.get('device_ui_id'), replace_existing=True)

    @classmethod
    def _cron_scheduler(cls, user_id, request_args):
        """
        Run a job when current time matches all specified time constraints, similarly to UNIX cron scheduler.

        :param (int) user_id: The user ID.
        :param (dict) request_args: The request arguments.
        """
        scheduler.add_job(cls._device_switch_util, args=(user_id, request_args.get('device_ui_id'), request_args.get('action')),
                          trigger=request_args.get('trigger'), year=request_args.get('year'), month=request_args.get('month'),
                          day=request_args.get('day'), week=request_args.get('week'), day_of_week=request_args.get('day_of_week'),
                          hour=request_args.get('hours'), minute=request_args.get('minutes'), second=request_args.get('seconds'),
                          start_date=request_args.get('start_date'), end_date=request_args.get('end_date'), id=request_args.get('device_ui_id'), replace_existing=True)

    @staticmethod
    def _device_switch_util(user_id, device_ui_id, device_status):
        """
        Common function to switch on/off device.

        :param (int) user_id: The user ID.
        :param (str) device_id: The lectical device unique ID.
        :param (str) mqtt_topic: The MQTT topic of the device.
        :param (str) device_status: The status to switch the device (on/off)
        """
        # Retrieve the related MQTT topic.
        mqtt_topic = DeviceModel.find_device_mqtt_topic(device_ui_id)
        if not mqtt_topic:
            return (dict(message='ERROR: Invalid device_ui_id. No related MQTT topic found.'), 404)

        # User requested to toggle the status of the device.
        if device_status == constants.DEVICE_TOGGLE:
            app.logger.info("Toggle smart socket.")
            # Retrieve current device status.
            device_status = DeviceModel.find_device_status(device_ui_id)
            # Toggle status.
            device_status = constants.DEVICE_TOGGLE_SWITCH.get(device_status)

        app.logger.info("Switch {} smart socket.".format(device_status))
        mqtt.mqttc.publish(mqtt_topic, constants.DEVICE_STATUS_CODE.get(device_status))

        fields_dict_to_update = dict(switch_state=constants.DEVICE_STATUS_SWITCH.get(
            device_status), status=device_status)

        if config.CACHE_ENABLED:
            devices_cache.update_cache(user_id, device_ui_id, fields_dict_to_update)

        return DeviceModel.update_device(device_ui_id, fields_dict_to_update)


class WifiSwitchStatus(Resource):
    """ Get the status of the device. """

    @jwt_required
    @swag_from('swagger/wifi_switch_status_swag.yml')
    def get(self, device_ui_id, action):
        """ GET request that requires JWT to retrieve device data for user. """

        app.logger.debug("Resource WifiSwitchAction GET.")

        # Retrieve the username from the JWT and find the current user from DB.
        current_user = UserModel.find_by_username(get_jwt_identity())

        # Retrieve the related MQTT topic.
        mqtt_topic = DeviceModel.find_device_mqtt_topic(device_ui_id)
        if not mqtt_topic:
            return (dict(message='ERROR: Invalid device_ui_id. No related MQTT topic found.'), 404)

        # User requested the status of the device.
        if action == constants.DEVICE_STATUS:
            app.logger.info(
                "Refresh: get smart socket status, saved in cache, if exists, else from db.")

            device_status = devices_cache.find_device_status(
                current_user.id, device_ui_id) if config.CACHE_ENABLED else DeviceModel.find_device_status(device_ui_id)
            return dict(message='Socket status is: %s.' % device_status, status=device_status, switch_state=constants.DEVICE_STATUS_SWITCH.get(device_status))

        # User requested to refresh and return the status of the device.
        if action == constants.DEVICE_REFRESH_STATUS:
            app.logger.info("Refresh: get smart socket status, saved in DB.")
            # Ask device to return its status.
            mqtt.mqttc.publish(mqtt_topic, constants.STATUS_DEVICE)
            time.sleep(5)  # TODO: Change logic.
            device_status = DeviceModel.find_device_status(device_ui_id)
            return dict(message='Socket status is: %s.' % device_status, status=device_status, switch_state=constants.DEVICE_STATUS_SWITCH.get(device_status))

        return (dict(message='ERROR: Invalid URL.'), 404)
