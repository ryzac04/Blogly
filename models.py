from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE = "https://www.freeiconspng.com/uploads/msn-people-person-profile-user-icon--icon-search-engine-11.png"


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(20), nullable=False)

    last_name = db.Column(db.String(20))

    image_url = db.Column(db.String, nullable=False, default=DEFAULT_IMAGE)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Blog post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)


class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    post = db.relationship(
        "Post",
        secondary="posts_tags",
        cascade="all,delete",
        backref="tags",
    )
