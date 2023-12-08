"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

app.config["SECRET_KEY"] = "not-a-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# User Routes


@app.route("/")
def root():
    """Redirect to users list."""
    return redirect("/users")


@app.route("/users")
def show_users():
    """Shows list of all users in db."""

    users = User.query.all()
    return render_template("users/index.html", users=users)


@app.route("/users/new")
def new_user():
    """Form for new users"""
    return render_template("users/new.html")


@app.route("/users/new", methods=["POST"])
def handle_form():
    """Submits form, creating new user and redirecting to list of all users."""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def user_profile(user_id):
    """Show user profile with a delete and edit button."""

    user = User.query.get_or_404(user_id)
    return render_template("users/details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_profile(user_id):
    """Show page allowing user to edit profile info."""

    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def handle_edit(user_id):
    """Updates user information and redirects to list of all users."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete an existing user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


# Posts Routes


@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)

    return render_template("posts/post.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def handle_post(user_id):
    """Handle submission of a user's post."""

    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, author_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show posted content in new page."""

    post = Post.query.get_or_404(post_id)

    return render_template("posts/show.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Show form to edit a post."""

    edit_post = Post.query.get_or_404(post_id)

    return render_template("posts/edit.html", edit_post=edit_post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def handle_edit_post(post_id):
    """Handle edit form to alter existing post content."""

    post = Post.query.get_or_404(post_id)

    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Deletes post."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.author_id}")
