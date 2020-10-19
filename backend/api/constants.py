"""
This module contains the constants of the application.
"""

DEVICE_SWITCH_STATE_ON = True
DEVICE_SWITCH_STATE_OFF = False
DEVICE_STATUS_ON = "on"
DEVICE_STATUS_OFF = "off"
DEVICE_TOGGLE = "toggle"
DEVICE_STATUS = "status"
DEVICE_REFRESH_STATUS = "refresh_status"

# Associate status "on" to True and "off" to False.
DEVICE_STATUS_SWITCH = dict()
DEVICE_STATUS_SWITCH[DEVICE_STATUS_ON] = DEVICE_SWITCH_STATE_ON
DEVICE_STATUS_SWITCH[DEVICE_STATUS_OFF] = DEVICE_SWITCH_STATE_OFF

CLOSE_DEVICE = "0"
START_DEVICE = "1"
STATUS_DEVICE = "2"

# MQTT TOPICS
UPDATE_SSID_PASS_TOPIC = 'esp8266/ssid/passwd'

# Aligned with devices firmware.
DEVICES_STATUS_TOPIC = 'esp8266/socket/status'

DOOR_TOPIC = 'esp8266/door'
