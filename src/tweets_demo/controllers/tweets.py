from flask import Flask, Blueprint, session, jsonify, render_template, url_for, request, redirect, flash
import ipdb


from datetime import datetime

tweets_blueprint = Blueprint("tweets", __name__)

from tweets_demo.app import db
from tweets_demo import login_required


@tweets_blueprint.route("/tweet/<id>")
@login_required
def show(id):
    from tweets_demo.models.tweet import Tweet
    from tweets_demo.models.user import User
    from tweets_demo.models.comment import Comment

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
    return render_template(
        "tweet/show.html", tweet=tweet, all_comments=all_comments, mess=mess, logedin_user_id=logedin_user_id
    )


@tweets_blueprint.route("/tweet/new")
@login_required
def new():
    return render_template("/tweet/new.html")


@tweets_blueprint.route("/tweet/new", methods=["POST"])
@login_required
def create():
    from tweets_demo.models.tweet import Tweet

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
        tweet = Tweet(
            id_user=session["logged_in"]["user_id"],
            created_at=str(current_date_time),
            content=request.form.get("content"),
        )
        flash("Tweet added")
        db.session.add(tweet)
        db.session.commit()
    except AssertionError as errors:
        return render_template("/tweet/new.html", errors=errors)
    return redirect("/")


@tweets_blueprint.route("/tweet/<id>/delete", methods=["GET", "POST"])
@login_required
def delete(id):
    from tweets_demo.models.tweet import Tweet
    from tweets_demo.models.comment import Comment

    tweet = Tweet.query.filter(Tweet.id == id).first()
    comments = Comment.query.filter(Comment.id_tweet == id).all()

    flash("Tweet and comments removed")
    for comment in comments:
        db.session.delete(comment)
        # db.session.commit()

    db.session.delete(tweet)
    db.session.commit()
    return redirect("/")
