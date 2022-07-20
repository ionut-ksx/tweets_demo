from flask import session, redirect, flash, url_for, render_template
from tweets_demo.models.user import User
from datetime import datetime
from functools import wraps


def current_user():
    current_user_id = int(session.get("logged_in", dict()).get("user_id", -1))
    return User.query.filter_by(id=current_user_id).first()


def current_date():
    x = datetime.now()
    current_date_time = x.strftime("%d-%m-%Y %H:%M")
    return str(current_date_time)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = current_user()
        if user:
            return f(user, *args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for("users.login"))

    return decorated


def my_render_template(*args, **kwargs):
    user = current_user()
    return render_template(*args, current_user=user, **kwargs)
