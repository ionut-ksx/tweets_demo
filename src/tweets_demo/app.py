from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
import time
import sys
from tweets_demo.configuration import config
import os


UPLOAD_FOLDER = "/tmp"

app = Flask(__name__)
app.secret_key = "SQLAlchemySecret"
app.config.update(config().as_dict())

db = SQLAlchemy(app)

from tweets_demo.controllers.tweets import tweets_blueprint
from tweets_demo.controllers.home import home_blueprint
from tweets_demo.controllers.users import users_blueprint
from tweets_demo.controllers.comments import comments_blueprint


app.register_blueprint(tweets_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(comments_blueprint)

if __name__ == "__main__":

    os.environ["FLASK_ENV"] = "development"
    os.environ["FLASK_APP"] = "app"
    app.run(debug=True)
