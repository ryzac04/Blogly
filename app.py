"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

app.config["SECRET_KEY"] = "not-a-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


###############################################################################
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


###############################################################################
# Post Routes


@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("posts/post.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def handle_post(user_id):
    """Handle submission of a user's post."""

    title = request.form["title"]
    content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=title, content=content, author_id=user_id, tags=tags)

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
    tags = Tag.query.all()

    return render_template("posts/edit.html", edit_post=edit_post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def handle_edit_post(post_id):
    """Handle edit form to alter existing post content."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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


###############################################################################
# Tag Routes


@app.route("/tags")
def show_tags():
    """Page displaying list of tags."""

    tags = Tag.query.all()

    return render_template("/tags/index.html", tags=tags)


@app.route("/tags/new")
def new_tag():
    """Form to add a new tag."""

    posts = Post.query.all()

    return render_template("/tags/new.html", posts=posts)


@app.route("/tags/new", methods=["POST"])
def handle_new_tag():
    """Submit new tag form, adding new tags to list."""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form["tag_name"], post=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    """Show details about a tag."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("/tags/show.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    """Edit form for a tag."""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template("/tags/edit.html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def handle_edit_tag(tag_id):
    """Submit the tag edit form with updated content."""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["tag_name"]
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag."""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
