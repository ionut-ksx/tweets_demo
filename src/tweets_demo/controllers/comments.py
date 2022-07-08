from flask import Flask, Blueprint, session, jsonify, render_template, url_for, request, redirect, flash
import ipdb


from datetime import datetime

comments_blueprint = Blueprint("comments", __name__)

from tweets_demo.app import db
from tweets_demo import login_required


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
            id_user=2,
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
