from initialization import db


class UserDevice():
    """
    User and devices have a Many-to-Many relationship,
    so here a link table is defined. As recommended in the documentation
    we do not use a model, but an actual table instead.
    Reference: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships
    """
    user_devices = db.Table('user_devices',
                            db.Column('user_id', db.Integer, db.ForeignKey(
                                'users.id'), primary_key=True),
                            db.Column('device_id', db.Integer, db.ForeignKey(
                                'devices.id'), primary_key=True)
                            )

    @classmethod
    def new_entry(cls, user_id, device_id):
        """
        Execute query to save a new entry in DB.

        :param (int) user_id: The user id.
        :param (int) device_id: The related device id.
        """
        user_devices_statement = cls.user_devices.insert().values(user_id=user_id, device_id=device_id)
        db.session.execute(user_devices_statement)
        db.session.commit()
