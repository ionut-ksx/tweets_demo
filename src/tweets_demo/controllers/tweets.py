from flask import Flask, Blueprint, session, jsonify, render_template, url_for, request, redirect, flash
import ipdb


tweets_blueprint = Blueprint("tweets", __name__)

from tweets_demo.app import db
from tweets_demo.controllers.application import current_date, login_required, my_render_template
from tweets_demo.models.tweet import Tweet
from tweets_demo.models.user import User
from tweets_demo.models.comment import Comment


@tweets_blueprint.route("/feed")
@login_required
def index(current_user):
    return my_render_template("tweets/index.html", tweets=current_user.tweets, user=current_user)


@tweets_blueprint.route("/tweets/<id>")
@login_required
def show(current_user, id):
    tweet_query = (
        Tweet.query.join(User, User.id == Tweet.id_user)
        .filter(Tweet.id == id)
        .add_columns(User.name, User.username, Tweet.content, Tweet.id, Tweet.id_user)
        .all()
    )
    tweet = tweet_query[0]

    all_comments = (
        User.query.join(Comment, Comment.id_user == User.id)
        .filter(Comment.id_tweet == id)
        .add_columns(Comment.content, Comment.id, Comment.id_user, User.name, User.username)
        .all()
    )
    logedin_user_id = session["logged_in"]["user_id"]
    mess = ""
    if len(all_comments) == 0:
        mess = "No comments to this tweet"
    return my_render_template(
        "tweets/show.html",
        tweet=tweet,
        all_comments=all_comments,
        mess=mess,
        logedin_user_id=logedin_user_id,
    )


@tweets_blueprint.route("/tweets/new")
@login_required
def new(current_user):
    return my_render_template("/tweets/new.html")


@tweets_blueprint.route("/tweets/new", methods=["POST"])
@login_required
def create(current_user):
    tweet = Tweet(
        id_user=session["logged_in"]["user_id"],
        created_at=current_date(),
        content=request.form.get("content"),
    )
    if tweet.is_valid:
        flash("Tweet added")
        db.session.add(tweet)
        db.session.commit()
        return redirect("/")
    else:
        return my_render_template("/tweets/new.html", errors=errors)


@tweets_blueprint.route("/tweets/<id>/delete", methods=["POST"])
@login_required
def destroy(current_user, id):
    tweet = Tweet.query.filter(Tweet.id == id).first()
    comments = Comment.query.filter(Comment.id_tweet == id).all()

    flash("Tweet and comments removed")
    for comment in comments:
        db.session.delete(comment)
        # db.session.commit()

    db.session.delete(tweet)
    db.session.commit()
    return redirect("/feed")
