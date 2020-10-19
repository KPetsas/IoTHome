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

        # Retrieve the related MQTT topic.
        mqtt_topic = DeviceModel.find_device_mqtt_topic(device_ui_id)
        if not mqtt_topic:
            return (dict(message='ERROR: Invalid device_ui_id. No related MQTT topic found.'), 404)

        # User requested to turn the device ON.
        if action == constants.DEVICE_STATUS_ON:
            app.logger.info("Switch on smart socket.")
            mqtt.mqttc.publish(mqtt_topic, constants.START_DEVICE)

            fields_dict_to_update = dict(switch_state=constants.DEVICE_STATUS_SWITCH.get(
                constants.DEVICE_STATUS_ON), status=constants.DEVICE_STATUS_ON)

            if config.CACHE_ENABLED:
                devices_cache.update_cache(current_user.id, device_ui_id, fields_dict_to_update)

            return DeviceModel.update_device(device_ui_id, fields_dict_to_update)

        # User requested to turn the device OFF.
        if action == constants.DEVICE_STATUS_OFF:
            app.logger.info("Switch off smart socket.")
            mqtt.mqttc.publish(mqtt_topic, constants.CLOSE_DEVICE)

            fields_dict_to_update = dict(switch_state=constants.DEVICE_STATUS_SWITCH.get(
                constants.DEVICE_STATUS_OFF), status=constants.DEVICE_STATUS_OFF)

            if config.CACHE_ENABLED:
                devices_cache.update_cache(current_user.id, device_ui_id, fields_dict_to_update)

            return DeviceModel.update_device(device_ui_id, fields_dict_to_update)

        # User requested to toggle the status of the device.
        if action == constants.DEVICE_TOGGLE:
            app.logger.info("Toggle smart socket.")
            device_status = DeviceModel.find_device_status(device_ui_id)

            if device_status == constants.DEVICE_STATUS_SWITCH.get(constants.DEVICE_SWITCH_STATE_ON):
                mqtt.mqttc.publish(mqtt_topic, constants.CLOSE_DEVICE)
                status = constants.DEVICE_STATUS_OFF
            else:
                mqtt.mqttc.publish(mqtt_topic, constants.START_DEVICE)
                status = constants.DEVICE_STATUS_ON

            fields_dict_to_update = dict(
                switch_state=constants.DEVICE_STATUS_SWITCH.get(status), status=status)

            if config.CACHE_ENABLED:
                devices_cache.update_cache(current_user.id, device_ui_id, fields_dict_to_update)

            return DeviceModel.update_device(device_ui_id, fields_dict_to_update)

        return (dict(message='ERROR: Invalid URL.'), 404)


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
