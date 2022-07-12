from flask import Flask, Blueprint, jsonify, render_template, url_for, request, redirect, flash, session
from werkzeug.utils import secure_filename

from tweets_demo.models.tweet import Tweet
from tweets_demo.models.user import User
from tweets_demo.services.search import SearchItem

from tweets_demo import login_required

import os
import ipdb


home_blueprint = Blueprint("home", __name__)
from tweets_demo.app import db


@home_blueprint.route("/")
@login_required
def index():
    # tweets = Tweet.query.order_by(Tweet.id).all()
    tweets = (
        Tweet.query.join(User, User.id == Tweet.id_user)
        .add_columns(User.name, User.username, Tweet.content, Tweet.id)
        .all()
    )
    return render_template("index.html", tweets=tweets)


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
