"""
    create users table
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship, validates
from tweets_demo.app import db
from werkzeug.security import generate_password_hash, check_password_hash
import re


class Role:
    ADMIN = 0
    USER = 1


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    pwhash = Column(String(255), nullable=False)
    role = Column(String(255), default=1)

    def __init__(self, username="", name="", pwhash="", role=Role.USER):
        self.username = self._username(username)
        self.name = self._name(name)
        self.pwhash = generate_password_hash(pwhash)
        self.role = role

    def __repr__(self):
        return f"id:{self.id}, username:{self.username}, name:{self.name}, role:{self.role}"

    @property
    def password(self):
        raise AttributeError("Password error")

    @password.setter
    def password(self, password):
        self.pwhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

    # check if the user is Admin
    def is_admin(self):
        return self.role == Role.ADMIN

    def _username(self, username):
        if not len(username) >= 5:
            raise ValueError("username should have at least 5 characters")
        return username

    def _name(self, name):
        name = name.strip()
        regex = "^[a-zA-Z]+$"
        if not re.match(regex, name):
            raise ValueError("Only letters are accepted")
        return name
