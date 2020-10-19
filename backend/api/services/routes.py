from router import Router
from services import wifi_switch_controller, door_opener_controller
# from services import *


class ServicesRouter(Router):
    """ Application services router class. """

    def register_routes(self, api):
        """ Register and relate controllers to the service endpoints. """

        # Smart switch
        api.add_resource(wifi_switch_controller.WifiSwitchAction, '/wifi-switches')
        api.add_resource(wifi_switch_controller.WifiSwitchStatus, '/<device_ui_id>/<action>')
        # Door opener
        api.add_resource(door_opener_controller.DoorOpener, '/door-opener')
