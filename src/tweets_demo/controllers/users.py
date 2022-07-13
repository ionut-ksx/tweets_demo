from flask import Flask, Blueprint, session, jsonify, render_template, url_for, request, redirect, flash
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash
import ipdb

from tweets_demo.models.user import User, Role
from tweets_demo.app import db
from tweets_demo.controllers.application import current_user


users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/login")
def login_form():
    return render_template("/forms/login.html")


@users_blueprint.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if user.check_password(password):
        flash("You are logged in", "success")
        set_login_session(user)
        return redirect(url_for("home.index"))
    else:
        flash("Username/password is wrong")
        return redirect(url_for("users.login"))


@users_blueprint.route("/register")
def register_form():
    return render_template("/forms/register.html")


def set_login_session(user):
    session["logged_in"] = {"user_id": user.id}


@users_blueprint.route("/register", methods=["POST"])
def register():
    if current_user():
        flash("Logout first")
        return render_template("home.index")

    username = request.form.get("username").lower()
    name = request.form.get("name")
    password = request.form.get("password")
    password_confirmation = request.form.get("re_password")

    user = User(username, name, password, password_confirmation, role=Role.USER)
    if user.is_valid():
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        flash("Successfully registered!")
        set_login_session(user)
        return redirect(url_for("home.index"))
    flash("Something went wrong!")
    return render_template("/forms/register.html", error=user.errors)


@users_blueprint.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logged out successfully")
    return redirect("/")
