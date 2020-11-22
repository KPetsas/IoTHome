"""
This module contains the constants of the application.
"""

_DEVICE_SWITCH_STATE_ON = True
_DEVICE_SWITCH_STATE_OFF = False
DEVICE_STATUS_ON = "on"
DEVICE_STATUS_OFF = "off"
DEVICE_TOGGLE = "toggle"
DEVICE_STATUS = "status"
DEVICE_REFRESH_STATUS = "refresh_status"

# Associate status "on" to True and "off" to False.
DEVICE_STATUS_SWITCH = dict()
DEVICE_STATUS_SWITCH[DEVICE_STATUS_ON] = _DEVICE_SWITCH_STATE_ON
DEVICE_STATUS_SWITCH[DEVICE_STATUS_OFF] = _DEVICE_SWITCH_STATE_OFF

# Switch on to off and vice versa.
DEVICE_TOGGLE_SWITCH = dict()
DEVICE_TOGGLE_SWITCH[DEVICE_STATUS_ON] = DEVICE_STATUS_OFF
DEVICE_TOGGLE_SWITCH[DEVICE_STATUS_OFF] = DEVICE_STATUS_ON

_CLOSE_DEVICE = "0"
_START_DEVICE = "1"
STATUS_DEVICE = "2"

# Associate status "on" to 1 and "off" to 0.
DEVICE_STATUS_CODE = dict()
DEVICE_STATUS_CODE[DEVICE_STATUS_ON] = _START_DEVICE
DEVICE_STATUS_CODE[DEVICE_STATUS_OFF] = _CLOSE_DEVICE

# MQTT TOPICS
UPDATE_SSID_PASS_TOPIC = 'esp8266/ssid/passwd'

# Aligned with devices firmware.
DEVICES_STATUS_TOPIC = 'esp8266/socket/status'

DOOR_TOPIC = 'esp8266/door'

# Datetime comma separated values.
DATETIME_CSV = ('year', 'month', 'day', 'hours', 'minutes', 'seconds')
