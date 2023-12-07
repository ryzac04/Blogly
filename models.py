from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

db = SQLAlchemy()

DEFAULT_IMAGE = "https://www.freeiconspng.com/uploads/msn-people-person-profile-user-icon--icon-search-engine-11.png"


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site user model."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(20), nullable=False)

    last_name = db.Column(db.String(20))

    image_url = db.Column(db.String, nullable=False, default=DEFAULT_IMAGE)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
