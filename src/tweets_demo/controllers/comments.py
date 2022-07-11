from flask import Flask, Blueprint, session, jsonify, render_template, url_for, request, redirect, flash
import ipdb
from sqlalchemy import delete


from datetime import datetime

comments_blueprint = Blueprint("comments", __name__)

from tweets_demo.app import db
from tweets_demo import login_required


@comments_blueprint.route("/comment/<id>")
@login_required
def show(id):
    from tweets_demo.models.user import User
    from tweets_demo.models.comment import Comment

    comment_query = (
        Comment.query.join(User, User.id == Comment.id_user)
        .filter(Comment.id == id)
        .add_columns(User.name, User.username, Comment.content, Comment.id)
        .all()
    )
    comment = comment_query[0]
    author = session["logged_in"]["user_id"]
    # if session["logged_in"]["user_id"] == comment.id_user:
    #     author = True
    return render_template("comment/show.html", comment=comment)


@comments_blueprint.route("/comment/new/<id>")
@login_required
def new(id):
    return render_template("/comment/new.html")


@comments_blueprint.route("/comment/new/<id>", methods=["POST"])
@login_required
def create(id):
    from tweets_demo.models.comment import Comment

    x = datetime.now()
    current_date_time = (
        x.strftime("%d")
        + "-"
        + x.strftime("%m")
        + "-"
        + x.strftime("%Y")
        + " "
        + x.strftime("%H")
        + ":"
        + x.strftime("%M")
    )
    try:
        comment = Comment(
            id_user=session["logged_in"]["user_id"],
            id_tweet=id,
            created_at=str(current_date_time),
            content=request.form.get("content"),
        )
        flash("Comment added")
        db.session.add(comment)
        db.session.commit()
    except AssertionError as errors:
        return render_template("/comment/new.html", errors=errors)
    return redirect("/")


@comments_blueprint.route("/comment/<id>/delete", methods=["GET", "POST"])
@login_required
def delete_C(id):
    from tweets_demo.models.comment import Comment

    comment = Comment.query.filter(Comment.id == id).first()

    flash("Comment removed")
    db.session.delete(comment)
    db.session.commit()
    return redirect("/")
