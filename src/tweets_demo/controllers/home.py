from flask import Flask, Blueprint, jsonify, render_template, url_for, request, redirect, flash, session
from werkzeug.utils import secure_filename

from tweets_demo.models.tweet import Tweet
from tweets_demo.models.user import User
from tweets_demo.services.search import SearchItem
from tweets_demo.controllers.application import current_user

from tweets_demo import login_required

import os
import ipdb


home_blueprint = Blueprint("home", __name__)
from tweets_demo.app import db


@login_required
@home_blueprint.route("/")
def index():
    # tweets = Tweet.query.order_by(Tweet.id).all()
    tweets = (
        Tweet.query.join(User, User.id == Tweet.id_user)
        .add_columns(User.name, User.username, Tweet.content, Tweet.id)
        .all()
    )
    if current_user():
        username = current_user().username
    else:
        username = "guest"
    return render_template("index.html", tweets=tweets, username=username)


@home_blueprint.route("/logout/")
@login_required
def logout():
    session.pop("logged_in", None)
    flash("Logged out successfully")
    return redirect(url_for("home.index"))


@home_blueprint.route("/results", methods=["GET", "POST"])
def search_results():
    search_string = request.args.get("q")
    ipdb.set_trace()
    service = SearchItem()
    results = service.search(search_string)

    return render_template(
        "services/search_results.html",
        results=results,
    )
