import constants

from flask_restful import Resource
from flask_jwt_extended import jwt_required

from run import mqtt
from app_initialization import app


# EXAMPLE URL: http://192.168.1.50:9191/api/door_opener
class DoorOpener(Resource):
    """ This service is responsible for opening the building door. """
    @jwt_required
    def get(self):
        """ GET request that requires JWT. """
        app.logger.info("Opening the building door.")
        mqtt.mqttc.publish(constants.DOOR_TOPIC, "1")
        return dict(status=200, message='Opening the building door...')
