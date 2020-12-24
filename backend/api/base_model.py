from datetime import datetime

from api.initialization import db


class BaseModel(db.Model):
    """
    Abstract class with common attributes, to be inherited by most db models.
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=True)

    def save_to_db(self):
        """ Common method for model classes to save model in DB. """
        db.session.add(self)
        db.session.commit()
