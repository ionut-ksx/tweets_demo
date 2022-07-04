from flask import Flask, Blueprint, session, jsonify, render_template, url_for, request, redirect, flash
import ipdb
from tweets_demo.models.tweets import Tweet
from tweets_demo.app import db


tweets_blueprint = Blueprint("tweets", __name__)


@users_blueprint.route("/tweet")
def tweet():
    pass
