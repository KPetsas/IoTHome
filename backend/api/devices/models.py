from sqlalchemy_serializer import SerializerMixin

from api.initialization import logger, db
from api.base_model import BaseModel
from api.user_devices.models import UserDevice


class DeviceModel(BaseModel, SerializerMixin):
    __tablename__ = 'devices'

    # Required info for the frontend of the application.
    serialize_only = ('device_ui_id', 'name', 'state', 'status', 'switch_state')

    # device_ui_id: e.g. security_alarm
    device_ui_id = db.Column(db.String(120), unique=True, nullable=False)
    # name: e.g. Security Alarm
    name = db.Column(db.String(120), nullable=False)
    # state: e.g. online
    state = db.Column(db.String(120), nullable=False)
    # status: e.g. disarmed, on, off
    status = db.Column(db.String(120), nullable=False)
    # switch_state: e.g. False (which means off)
    switch_state = db.Column(db.Boolean, nullable=False)
    # button_type: e.g. switch or btn_timer etc
    button_type = db.Column(db.String(120), nullable=False)
    # mqtt_topic: e.g. esp8266/socket
    mqtt_topic = db.Column(db.String(120), nullable=False)
    # In case of e.g. alarm system it may be useful to know who has enable/disable the alarm last.
    # last_user_id = db.Column(db.Integer, nullable=True)

    user = db.relationship('UserModel',
                           secondary=UserDevice.user_devices,
                           lazy='subquery',
                           backref=db.backref('users', lazy=True)
                           )

    @classmethod
    def update_device(cls, device_ui_id, fields_dict, return_obj=True):
        """
        Update the device model and return it.

        :param (str) device_ui_id: The unique device id used in UI.
        :param (dict) fields_dict: The fields to update in the retrieved device model.
        :param (bool) return_obj: Optional, flag to return the device model or not.
        :return: DeviceModel
        """
        logger.debug("DB: Update the device model and save it in DB.")
        device = cls.__find_by_device_ui_id(device_ui_id)
        device.update(fields_dict)
        db.session.commit()
        if return_obj:
            return device.first().to_dict()

    @classmethod
    def return_user_devices(cls, user_id):
        """
        Retrieve all the user devices from DB.

        :param (int) user_id: The current user id.
        :return: list of user devices.
        """
        logger.debug("DB: Retrieve all user devices from DB.")
        all_user_devices = cls.query.join(cls.user).filter_by(id=user_id).all()
        return list(map(lambda device_data: device_data.to_dict(), all_user_devices))

    @classmethod
    def find_user_has_device(cls, device_ui_id, user):
        """
        Verify if device exists for user in DB.

        :param (str) device_ui_id: The unique device id used in UI.
        :param (str) user: The username of the user.
        """
        logger.debug("DB: Find if user has device.")
        return cls.__find_by_device_ui_id(device_ui_id).join(cls.user).filter_by(username=user).first()

    @classmethod
    def find_device_id(cls, device_ui_id):
        """
        Retrieve the device id from DB.

        :param (str) device_ui_id: The unique device id used in UI.
        :return: (int) device id.
        """
        logger.debug("DB: Retrieve the device ID from DB.")
        device = cls.__find_by_device_ui_id(device_ui_id).first()
        return device.id if device else device

    @classmethod
    def find_device_mqtt_topic(cls, device_ui_id):
        """
        Retrieve the device related MQTT topic from DB.

        :param (str) device_ui_id: The unique device id used in UI.
        :return: (str) mqtt topic.
        """
        logger.debug("DB: Retrieve the device MQTT topic from DB.")
        device = cls.__find_by_device_ui_id(device_ui_id).first()
        return device.mqtt_topic if device else device

    @classmethod
    def find_device_status(cls, device_ui_id):
        """
        Retrieve the device status from DB.

        :param (str) device_ui_id: The unique device id used in UI.
        :return: (str) device status.
        """
        logger.debug("DB: Retrieve the device status from DB.")
        device = cls.__find_by_device_ui_id(device_ui_id).first()
        return device.status if device else device

    @classmethod
    def __find_by_device_ui_id(cls, device_ui_id):
        """ DB query filter by device_ui_id, which is unique, so it returns one entry. """
        return cls.query.filter_by(device_ui_id=device_ui_id)
