import config

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from app_initialization import app, devices_cache
from auth.models import UserModel
from devices.models import DeviceModel
from user_devices.models import UserDevice


class UserDeviceRegistration(Resource):
    """ Controller to help register a device to a user. """

    def __init__(self):
        """ Setup the request arguments parser in the constructor. """
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('device_ui_id', help='This field cannot be blank', required=True)
        self._parser.add_argument('name', help='This field cannot be blank', required=True)
        self._parser.add_argument('state', help='This field cannot be blank', required=True)
        self._parser.add_argument('status', help='This field cannot be blank', required=True)
        self._parser.add_argument('switch_state', help='This field cannot be blank', required=True)
        self._parser.add_argument('button_type', help='This field cannot be blank', required=True)
        self._parser.add_argument('mqtt_topic', help='This field cannot be blank', required=True)

    @jwt_required
    def post(self):
        """ POST request that requires JWT. """

        # Parse request arguments.
        data = self._parser.parse_args()

        # Retrieve the username from the JWT
        username = get_jwt_identity()
        # Find the current user from DB.
        current_user = UserModel.find_by_username(username)

        device_id = DeviceModel.find_device_id(data['device_ui_id'])

        user_has_device = DeviceModel.find_user_has_device(data['device_ui_id'], username)

        if user_has_device:
            return (dict(message='Device {} already exists for user {}'.format(data['device_ui_id'], username)), 200)

        if device_id:
            # If the device exists already, just relate it to the user.
            UserDevice.new_entry(current_user.id, device_id)
            return (dict(message='Device {} was added also for user {}'.format(data['device_ui_id'], username)), 200)
        else:
            # If the device does not exist, register it and relate it to the user.
            if config.CACHE_ENABLED:
                # Clear cache in order to reload with the new device.
                devices_cache.clear_user_cache(current_user.id)

            new_device = DeviceModel(
                device_ui_id=data['device_ui_id'],
                name=data['name'],
                state=data['state'],
                status=data['status'],
                switch_state=eval(data['switch_state'].capitalize()),
                button_type=data['button_type'],
                mqtt_topic=data['mqtt_topic'],
            )

            new_device.user.append(current_user)

            try:
                new_device.save_to_db()
                return (dict(message='Device {} was added for user {}'.format(data['device_ui_id'], username)), 201)
            except Exception as e:
                app.logger.error(e)
                return (dict(message='Something went wrong'), 500)
