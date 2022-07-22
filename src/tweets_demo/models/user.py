"""
    create users table
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Index, DateTime
from sqlalchemy.orm import relationship, validates
from tweets_demo.app import db
from werkzeug.security import generate_password_hash, check_password_hash
import re
from sqlalchemy.ext.declarative import declarative_base
import ipdb
import secrets
import string
from datetime import datetime, timedelta

Base = declarative_base()

char_string = string.ascii_letters + string.digits


def get_random_string(size):
    return "".join(secrets.choice(char_string) for _ in range(size))


def tomorrow():
    return datetime.now() + timedelta(hours=24)


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
    tweets = relationship("Tweet", primaryjoin="User.id==Tweet.id_user")
    comments = relationship("Comment", primaryjoin="User.id==Comment.id_user")
    email = Column(String(255), nullable=False)
    recovery_hash = Column(String(255), nullable=True)
    recovery_hash_expires_at = Column(DateTime(), nullable=True)

    def __init__(self, email, username="", name="", passwd="", password_confirmation="", role=Role.USER):
        self.email = email
        self.username = username
        self.errors = []
        self.name = name
        self.password(passwd, password_confirmation)
        self.role = role

    def prepare_for_trouble(self):
        if not getattr(self, "errors", None):
            self.errors = []

    @validates(
        "email",
        "username",
        "name",
        "pwhash",
        "role",
    )
    def validates_fields(self, key, value):
        self.prepare_for_trouble()

        if not value:
            self.errors.append(f"{key} is missing")

        if key == "email":
            if "@" not in value:
                self.errors.append("email must contain @ character")

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
        # special_sym = ["$", "@", "#", "%"]

        if len(password) < 6:
            self.errors.append("length should be at least 6")

        # if not any(char.isdigit() for char in password):
        #     self.errors.append("Password should have at least one numeral")

        # if not any(char.isupper() for char in password):
        #     self.errors.append("Password should have at least one uppercase letter")

        # if not any(char.islower() for char in password):
        #     self.errors.append("Password should have at least one lowercase letter")

        # if not any(char in special_sym for char in password):
        #     self.errors.append("Password should have at least one of the symbols $@#")

    def persist(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()

    def recovery_hash_is_active(self):
        return self.recovery_hash and self.recovery_hash_expires_at > datetime.now()

    def prepare_for_recovery(self):
        self.prepare_for_trouble()

        if self.recovery_hash_is_active():
            self.errors.append("Can't request a new password right now")
            return

        self.recovery_hash = get_random_string(32)
        self.recovery_hash_expires_at = tomorrow()
        self.persist()
        return True

    def recover_password(self, passwd, password_confirmation):
        self.password(passwd, password_confirmation)
        self.recovery_hash = None
        self.recovery_hash_expires_at = None
        self.persist()
