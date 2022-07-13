from flask import Flask, Blueprint, session, jsonify, render_template, url_for, request, redirect, flash
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash
from tweets_demo.models.user import validate_password
import ipdb

from tweets_demo.models.user import User
from tweets_demo.app import db


users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/login")
def login_form():
    return render_template("/forms/login.html")


@users_blueprint.route("/login", methods=["POST"])
def login():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

    except AssertionError as error:
        return render_template("login.html", error=error)
    else:
        user = User.query.filter_by(username=username).first()
        if user.check_password(password):
            flash("You are logged in", "success")
            session["logged_in"] = {"username": user.username, "user_id": user.id}
            return redirect(url_for("home.index"))


@users_blueprint.route("/register")
def register_form():
    return render_template("/forms/register.html")


def set_login_session(user):
    session["logged_in"] = {"user_id": user.id}


@users_blueprint.route("/register", methods=["POST"])
def register():
    if session.get("logged_in"):
        flash("Logout first")
        return render_template("home.index")

    data = {
        "username": request.form.get("username").lower(),
        "name": request.form.get("name"),
        "password": request.form.get("password"),
        "re_password": request.form.get("re_password"),
    }
    if validate_password(data.get("password")):
        if data.get("password") == data.get("re_password"):
            check_user = User.query.filter_by(username=data.get("username")).first()
            if check_user == None:
                username = data.get("username")
                name = data.get("name")
                password = data.get("password")

                user = User(username, name, password, role=1)
                errors = user.errors

                if user.is_valid():
                    db.session.add(user)
                    db.session.flush()
                    db.session.commit()
                    flash("Successfully registered!")
                    set_login_session(user)
                    return redirect(url_for("home.index"))
                else:
                    print(errors)
                    return render_template("/forms/register.html", error=errors)

            else:
                flash("The username is already taken")
                return render_template("/forms/register.html")
        else:
            errors = "Password does not match!"
            return render_template("/forms/register.html", error=errors)
    else:
        errors = validate_password(data.get("password"))
        print(errors)
        return render_template("/forms/register.html", error=errors)


@users_blueprint.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logged out successfully")
    return redirect(url_for("users.login"))
