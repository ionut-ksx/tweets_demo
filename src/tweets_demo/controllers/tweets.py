from flask import Flask, Blueprint, session, jsonify, render_template, url_for, request, redirect, flash
import ipdb
from tweets_demo.models.tweet import Tweet
from tweets_demo.models.user import User
from tweets_demo.models.comment import Comment
from datetime import datetime

tweets_blueprint = Blueprint("tweets", __name__)

from tweets_demo.app import db


@tweets_blueprint.route("/tweet/<id>")
def show(id):
    query = Tweet.query.filter_by(id=id).all()
    tweet = query[0]

    author_query = User.query.filter_by(id=query[0].id_user).all()
    tweet_author = author_query[0]

    comments = Comment.query.filter_by(id_tweet=id).order_by(Comment.id).all()
    # author_list = []
    # for comment in comments:
    #     comment_author_query = User.query.filter_by(id=comment.id_user).all()
    #     author_list.append(comment_author_query[0])
    # print(author_list)
    print(comments)
    # all_comments = Comments.query.join(User).filter(User.id == comments.id_user).all()
    mess = ""
    # if len(all_comments) == 0:
    #     mess = "No comments to this tweet"
    return render_template("tweet/show.html", tweet=tweet, tweet_author=tweet_author, comments=comments, mess=mess)


@tweets_blueprint.route("/tweet/new")
def new():
    return render_template("/tweet/new.html")


@tweets_blueprint.route("/tweet/new", methods=["POST"])
def create():
    current_date_time = datetime.now()
    # current_date_time = x.strftime("%d") + "." + x.strftime(%m) + "." + x.strftime(%d) + " " + x.strftime(%H) + ":" + x.strftime(%M)
    try:
        tweet = Tweet(
            id_user=2,
            created_at=str(current_date_time),
            content=request.form.get("content"),
        )
        db.session.add(tweet)
        db.session.commit()
    except AssertionError as errors:
        return render_template("/tweet/new.html", errors=errors)
    return redirect("/")
