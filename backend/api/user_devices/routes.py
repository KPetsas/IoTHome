from api.user_devices import controllers
from api.router import Router


class UserDevicesRouter(Router):
    """ Devices related to users router class. """

    def register_routes(self, api):
        """ Register and relate user devices endpoints with controllers. """
        # Device Registration
        api.add_resource(controllers.UserDeviceRegistration, '/device-registration')
