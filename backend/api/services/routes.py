from api.router import Router
from api.services import wifi_switch_action_controller, wifi_switch_status_controller, door_opener_controller
# from api.services import *


class ServicesRouter(Router):
    """ Application services router class. """

    def register_routes(self, api):
        """ Register and relate controllers to the service endpoints. """

        # Smart switch
        api.add_resource(wifi_switch_action_controller.WifiSwitchAction, '/wifi-switches')
        api.add_resource(wifi_switch_status_controller.WifiSwitchStatus, '/<device_ui_id>/<action>')
        # Door opener
        api.add_resource(door_opener_controller.DoorOpener, '/door-opener')
