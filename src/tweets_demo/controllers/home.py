from flask import Flask, Blueprint, jsonify, render_template, url_for, request, redirect, flash, session
from werkzeug.utils import secure_filename

from tweets_demo.models.tweet import Tweet
from tweets_demo.models.user import User
from tweets_demo.services.search import SearchItem
from tweets_demo.controllers.application import current_user, login_required, my_render_template


import os
import ipdb


home_blueprint = Blueprint("home", __name__)
from tweets_demo.app import db


@home_blueprint.route("/mytweets")
@login_required
def my_tweets(current_user):
    user = current_user()
    tweets = user.tweets
    return render_template("tweet/my_tweets.html", tweets=tweets, username=user.username)


@home_blueprint.route("/")
@login_required
def index(current_user):
    # tweets = Tweet.query.order_by(Tweet.id).all()
    tweets = (
        Tweet.query.join(User, User.id == Tweet.id_user)
        .add_columns(User.name, User.username, Tweet.content, Tweet.id)
        .all()
    )
    return my_render_template("index.html", tweets=tweets)


@home_blueprint.route("/results", methods=["GET", "POST"])
@login_required
def search_results(current_user):
    search_string = request.args.get("q")
    service = SearchItem()
    results = service.search(search_string)

    return render_template(
        "services/search_results.html",
        results=results,
    )
