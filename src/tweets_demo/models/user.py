"""
    create users table
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship, validates
from tweets_demo.app import db


class Role:
    ADMIN = 1
    USER = 2


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    pwhash = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)

    def __repr__(self):
        return f"id:{self.id}, username:{self.username}, name:{self.name}, role:{self.role}"
