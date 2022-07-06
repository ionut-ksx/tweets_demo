from flask import Flask, Blueprint, jsonify, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
from tweets_demo.models.tweet import Tweet

import os
import ipdb


home_blueprint = Blueprint("home", __name__)
from tweets_demo.app import db


@home_blueprint.route("/")
def index():
    tweets = Tweet.query.order_by(Tweet.id).all()
    return render_template("index.html", tweets=tweets)
