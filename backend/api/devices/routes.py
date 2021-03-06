from api.devices import controllers
from api.router import Router


class DevicesRouter(Router):
    """ Devices router class. """

    def register_routes(self, api):
        """ Register and relate devices endpoints with controllers. """
        api.add_resource(controllers.Devices, '/devices')
