from unittest import TestCase

from app import app
from models import db, User

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

app.config["TESTING"] = True

app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests our model for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="John", last_name="Doe", image_url="www.someimage.com")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up after test."""

        db.session.rollback()

    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Doe", html)

    def test_new_user(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("First Name", html)

    def test_handle_form(self):
        with app.test_client() as client:
            resp = client.post(
                "/users/new",
                data={
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "image_url": "www.newphoto.com",
                },
            )

            user = User.query.filter_by(last_name="Smith").first()

            self.assertIn(user.first_name, "Jane")
            self.assertIn(user.image_url, "www.newphoto.com")

    def test_user_profile(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>John Doe</h1>", html)

    def test_edit_profile(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Edit User</h1>", html)

    def test_handle_edit(self):
        with app.test_client() as client:
            resp = client.post(
                f"/users/{self.user_id}/edit",
                data={
                    "first_name": "John",
                    "last_name": "Smith",
                    "image_url": "www.profilepic.com",
                },
            )
            user = User.query.filter_by(first_name="John").first()

            self.assertIn(user.first_name, "John")
            self.assertIn(user.image_url, "www.profilepic.com")
