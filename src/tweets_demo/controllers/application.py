from flask import session
from tweets_demo.models.user import User
from datetime import datetime


def current_user():
    current_user_id = int(session.get("logged_in", dict()).get("user_id", -1))
    return User.query.filter_by(id=current_user_id).first()


def current_date():
    x = datetime.now()
    current_date_time = x.strftime("%d-%m-%Y %H:%M")
    return str(current_date_time)
