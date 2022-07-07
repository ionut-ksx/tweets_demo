from flask import Flask, Blueprint, session, jsonify, render_template, url_for, request, redirect, flash
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
        # user = User.query.get(username)
        user = User.query.filter_by(username=username).first()
        # ipdb.set_trace()
        if user.check_password(password):
            flash("You are logged in", "success")
            session["logged_in"] = user.username
            return redirect(url_for("home.index"))


@users_blueprint.route("/register")
def register_form():
    return render_template("/forms/register.html")


@users_blueprint.route("/register", methods=["POST"])
def register():
    if session.get("logged_in"):
        flash("Logout first")
        return render_template("home.index")
    else:
        try:
            username = request.form.get("username")
            name = request.form.get("name")
            password = request.form.get("password")
            re_password = request.form.get("re_password")
        except AssertionError as error:
            return render_template("/forms/register.html", error=error)
        else:
            if password == re_password:
                check_user = User.query.filter_by(username=username).first()
                if check_user == None:
                    user = User(username, name, password, role=1)
                    db.session.add(user)
                    db.session.flush()
                    db.session.commit()
                    flash("Successfully registered!")
                    return redirect(url_for("home.index"))
                else:
                    flash("The username is already taken")
                    return render_template("/forms/register.html")


@users_blueprint.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logged out successfully")
    return redirect(url_for("users.login"))
