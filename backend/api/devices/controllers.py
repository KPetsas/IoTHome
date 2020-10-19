import config

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from app_initialization import app, devices_cache
from auth.models import UserModel
from devices.models import DeviceModel


# EXAMPLE URL: http://192.168.1.50:9191/api/devices
class Devices(Resource):
    """ Devices controller. """

    @jwt_required
    @swag_from('swagger/devices_swag.yml')
    def get(self):
        """ POST request that requires JWT. """

        app.logger.info("Get a list of the user devices.")

        # Retrieve the username from the JWT and find the current user from DB.
        current_user = UserModel.find_by_username(get_jwt_identity())

        if config.CACHE_ENABLED:
            # Get a list of the cached user devices.
            user_cached_devices = devices_cache.get_user_cache(current_user.id)

            devices = user_cached_devices if user_cached_devices else DeviceModel.return_user_devices(
                current_user.id)
            devices_cache.cache = (current_user.id, devices)
            return dict(devices=devices)

        return dict(devices=DeviceModel.return_user_devices(current_user.id))
