from flask import Flask, Blueprint, session, jsonify, render_template, url_for, request, redirect, flash
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash
import ipdb

from tweets_demo.models.user import User, Role
from tweets_demo.app import db
from tweets_demo.controllers.application import current_user, login_required, my_render_template
from tweets_demo.app import mail
from flask_mail import Message

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/login")
def login_form():
    if current_user():
        flash("Already logged in")
        return redirect(url_for("home.index"))
    return my_render_template("/forms/login.html", username="guest")


@users_blueprint.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    while user:
        if user.check_password(password):
            flash("You are logged in", "success")
            set_login_session(user)
            return redirect(url_for("home.index"))
        else:
            flash("Username/password is wrong")
            return redirect(url_for("users.login"))
    flash("Check your credentials")
    return redirect(url_for("users.login"))


@users_blueprint.route("/register")
def register_form():

    if current_user():
        flash("Logout first")
        return redirect(url_for("home.index"))
    else:
        username = "guest"
        return my_render_template("/forms/register.html", username="guest")


def set_login_session(user):
    session["logged_in"] = {"user_id": user.id}


@users_blueprint.route("/register", methods=["POST"])
def register():
    if current_user():
        flash("Logout first")
        return redirect(url_for("home.index"))

    email = request.form.get("email").lower()
    username = request.form.get("username").lower()
    name = request.form.get("name")
    password = request.form.get("password")
    password_confirmation = request.form.get("re_password")

    user = User(email, username, name, password, password_confirmation, role=Role.USER)
    if user.is_valid():
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        flash("Successfully registered!")
        set_login_session(user)
        return redirect(url_for("home.index"))
    flash("Something went wrong!")
    return my_render_template("/forms/register.html", error=user.errors, username="guest")


@users_blueprint.route("/recovery/request")
def request_recovery():
    return my_render_template("/forms/request_recovery.html")


@users_blueprint.route("/recovery/request", methods=["POST"])
def create_recovery_hash():
    email = request.form.get("email").lower()
    existing_user = User.query.filter_by(email=email).first()
    if not existing_user:
        raise ("touch luck")
    succes = existing_user.prepare_for_recovery()
    if succes:
        send_recovery_email(existing_user)
        flash("Successfully requested password!")
    else:
        flash(",".join(existing_user.errors))
    return my_render_template("/forms/request_recovery.html")


@users_blueprint.route("/recovery/")
def recovery_set_password():
    recovery_hash = request.args.get("recovery_hash")
    return my_render_template("/forms/set_recovery.html", recovery_hash=recovery_hash)


@users_blueprint.route("/recovery/", methods=["POST"])
def set_recovery():
    recovery_hash = request.form.get("recovery_hash")
    password = request.form.get("password")
    password_confirmation = request.form.get("password_confirmation")
    existing_user = User.query.filter_by(recovery_hash=recovery_hash).first()
    if not existing_user:
        flash("Invalid recovery token")
        return redirect("/")
    if existing_user.recovery_hash_is_active():
        existing_user.recover_password(password, password_confirmation)
        flash("Password reset successfully")
        return redirect("/login")


@users_blueprint.route("/logout")
@login_required
def logout(current_user):
    session.pop("logged_in", None)
    flash("Logged out successfully")
    return redirect("/")


def send_recovery_email(user):
    recovery_hash = user.recovery_hash
    msg = Message("Password recovery", sender="no-reply@tweets.demo", recipients=[user.email])
    msg.body = f"<a href='http://127.0.0.1:5001/recovery?recovery_hash={recovery_hash}'>Recover your password</a> "
    mail.send(msg)
