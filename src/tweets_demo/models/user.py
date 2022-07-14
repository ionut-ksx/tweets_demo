"""
    create users table
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship, validates
from tweets_demo.app import db
from werkzeug.security import generate_password_hash, check_password_hash
import re
from sqlalchemy.ext.declarative import declarative_base
import ipdb

Base = declarative_base()


class Role:
    ADMIN = 0
    USER = 1


class User(db.Model, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    pwhash = Column(String(255), nullable=False)
    role = Column(String(255), default=1)
    tweet = relationship("Tweet", primaryjoin="User.id==Tweet.id_user")
    comment = relationship("Comment", primaryjoin="User.id==Comment.id_user")

    def __init__(self, username="", name="", passwd="", password_confirmation="", role=Role.USER):
        self.username = username
        self.errors = []
        self.name = name
        self.password(passwd, password_confirmation)
        self.role = role

    @validates(
        "username",
        "name",
        "pwhash",
        "role",
    )
    def validates_fields(self, key, value):
        if not getattr(self, "errors", None):
            self.errors = []

        if not value:
            self.errors.append(f"{key} is missing")

        if key == "username":
            if not len(value) >= 5:
                self.errors.append(f"{key} should have at least 5 characters")
            existing_user = User.query.filter_by(username=value).first()
            if existing_user:
                self.errors.append("The username is already taken")

        if key == "name":
            name = value.strip()
            regex = "^[a-zA-Z]+[' '-]?[a-zA-Z]*([' '-]?[a-zA-Z])*$"
            if not re.match(regex, name):
                self.errors.append(f"ie. '{key}' format: Asterix-Obelix Idefix ")

        return value

    def __repr__(self):
        return f"id:{self.id}, username:{self.username}, name:{self.name}, role:{self.role}"

    @property
    def password(self):
        pass

    def password(self, password, password_confirmation):
        self.validate_password_confirmation(password, password_confirmation)
        self.validate_password(password)
        self.pwhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

    # check if the user is Admin
    def is_admin(self):
        return self.role == Role.ADMIN

    def is_valid(self):
        return len(self.errors) == 0

    def validate_password_confirmation(self, password, password_confirmation):
        if password != password_confirmation:
            self.errors.append("Password does not match password confirmation")

    def validate_password(self, password):
        special_sym = ["$", "@", "#", "%"]

        if len(password) < 6:
            self.errors.append("length should be at least 6")

        if not any(char.isdigit() for char in password):
            self.errors.append("Password should have at least one numeral")

        if not any(char.isupper() for char in password):
            self.errors.append("Password should have at least one uppercase letter")

        if not any(char.islower() for char in password):
            self.errors.append("Password should have at least one lowercase letter")

        if not any(char in special_sym for char in password):
            self.errors.append("Password should have at least one of the symbols $@#")
