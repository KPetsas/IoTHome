import time

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from api.configuration import settings as config
from api import constants
from api.initialization import logger, devices_cache, mqtt
from api.auth.models import UserModel
from api.devices.models import DeviceModel


class WifiSwitchStatus(Resource):
    """ Get the status of the device. """

    @jwt_required
    @swag_from('swagger/wifi_switch_status_swag.yml')
    def get(self, device_ui_id, action):
        """ GET request that requires JWT to retrieve device data for user. """

        logger.debug("Resource WifiSwitchAction GET.")

        # Retrieve the username from the JWT and find the current user from DB.
        current_user = UserModel.find_by_username(get_jwt_identity())

        # Retrieve the related MQTT topic.
        mqtt_topic = DeviceModel.find_device_mqtt_topic(device_ui_id)
        if not mqtt_topic:
            return (dict(message='ERROR: Invalid device_ui_id. No related MQTT topic found.'), 404)

        # User requested the status of the device.
        if action == constants.DEVICE_STATUS:
            logger.info("Refresh: get smart socket status, saved in cache, if exists, else from db.")

            if config.CACHE_ENABLED:
                device_status = devices_cache.find_device_status(current_user.id, device_ui_id)
                if not device_status:
                    device_status = DeviceModel.find_device_status(device_ui_id)
            else:
                device_status = DeviceModel.find_device_status(device_ui_id)

            return dict(message='Socket status is: %s.' % device_status, status=device_status, switch_state=constants.DEVICE_STATUS_SWITCH.get(device_status))

        # User requested to refresh and return the status of the device.
        if action == constants.DEVICE_REFRESH_STATUS:
            logger.info("Refresh: get smart socket status, saved in DB.")
            # Reload cache to update/sync all users devices.
            # devices_cache.clear_cache()
            # Ask device to return its status.
            mqtt.mqttc.publish(mqtt_topic, constants.STATUS_DEVICE)
            time.sleep(5)  # TODO: Change logic.
            device_status = DeviceModel.find_device_status(device_ui_id)
            return dict(message='Socket status is: %s.' % device_status, status=device_status, switch_state=constants.DEVICE_STATUS_SWITCH.get(device_status))

        return (dict(message='ERROR: Invalid URL.'), 404)
