import time

import config
import constants

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from run import mqtt
from app_initialization import app, devices_cache
from auth.models import UserModel
from devices.models import DeviceModel


# EXAMPLE URL: http://192.168.1.50:9191/api/wifi_switches
class WifiSwitchAction(Resource):
    """ Control every wifi switch through this controller. """

    def __init__(self):
        """ Setup the request arguments parser in the constructor. """
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('device_ui_id', help='This field cannot be blank', required=True)
        self._parser.add_argument('action', help='This field cannot be blank', required=True)

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
