from flask import session
from tweets_demo.models.user import User


def current_user():
    current_user_id = int(session.get("logged_in", dict()).get("user_id", -1))
    return User.query.filter_by(id=current_user_id).first()
