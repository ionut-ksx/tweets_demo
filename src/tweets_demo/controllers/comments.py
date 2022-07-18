from flask import Flask, Blueprint, session, jsonify, render_template, url_for, request, redirect, flash
import ipdb
from sqlalchemy import delete


from datetime import datetime

comments_blueprint = Blueprint("comments", __name__)

from tweets_demo.app import db
from tweets_demo import login_required
from tweets_demo.controllers.application import current_user, current_date
from tweets_demo.models.user import User
from tweets_demo.models.comment import Comment


@comments_blueprint.route("/comment/<id>")
@login_required
def show(id):

    comment_query = (
        Comment.query.join(User, User.id == Comment.id_user)
        .filter(Comment.id == id)
        .add_columns(User.name, User.username, Comment.content, Comment.id)
        .all()
    )
    comment = comment_query[0]
    author = session["logged_in"]["user_id"]
    return render_template("comment/show.html", comment=comment)


@comments_blueprint.route("/comment/new/<id>")
@login_required
def new(id):
    return render_template("/comment/new.html")


@comments_blueprint.route("/comment/new/<id>", methods=["POST"])
@login_required
def create(id):

    comment = Comment(
        id_user=session["logged_in"]["user_id"],
        id_tweet=id,
        created_at=current_date(),
        content=request.form.get("content"),
    )
    if comment.is_valid():
        flash("Comment added")
        db.session.add(comment)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("/comment/new.html", errors=errors)


@comments_blueprint.route("/comment/<id>/delete", methods=["GET", "POST"])
@login_required
def destroy(id):

    comment = Comment.query.filter(Comment.id == id).first()

    flash("Comment removed")
    db.session.delete(comment)
    db.session.commit()
    return redirect("/")
