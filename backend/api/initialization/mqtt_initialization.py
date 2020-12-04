import paho.mqtt.client as mqtt

import configuration.settings as config
import constants


class MQTT():
    """ Initialize the MQTT client. """

    def init_app(self, app):
        self._logger = app.logger

        self._logger.info("Initialize MQTT client: Connecting to %s:%s." %
                          (config.MQTT_IP, config.MQTT_PORT))

        # MQTT client for smart devices.
        self.mqttc = mqtt.Client()
        if config.CA_CERT_PATH:
            self.mqttc.tls_set(config.CA_CERT_PATH)
        self.mqttc.connect(config.MQTT_IP, config.MQTT_PORT, 60)

        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

        self.mqttc.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """ Retrieve the status of all the connected devices. """
        self._logger.info("Connected to devices status topic with result code {}".format(rc))
        client.subscribe(constants.DEVICES_STATUS_TOPIC)

    def on_message(self, client, userdata, msg):
        """ The message received from device is JSON with fields device_ui_id, status(e.g. on/off) """
        mqtt_message = msg.payload.decode()
        self._logger.info("MQTT client received message: {}".format(mqtt_message))
        mqtt_message_status = mqtt_message.get('status')
        # if mqtt_message_status in [constants.DEVICE_STATUS_ON, constants.DEVICE_STATUS_OFF]:
        # DeviceModel.update_device(mqtt_message.get('device_ui_id'), dict(
        #    switch_state=constants.DEVICE_STATUS_SWITCH.get(mqtt_message_status), status=mqtt_message_status), return_obj=False)
