import os
from flask_login import LoginManager
from functools import wraps
from flask_sessionstore import Session
from flask import session, url_for, redirect, flash

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for("users.login"))

    return wrap
