from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship, validates
from tweets_demo.app import db
from tweets_demo.models.user import User
import re


class Tweet(db.Model):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    id_user = Column(Integer, nullable=False)
    created_at = Column(String(255), nullable=False)
    content = Column(String(256), nullable=False)
    id_user = relationship("User", back_populates="id")

    def __init__(self, id_user="", created_at="", content=""):
        self.id_user = self._is_valid_id_user(str(id_user))
        self.created_at = self._is_valid_date_time(created_at)
        self.content = self._is_valid_content(content)

    def __repr__(self):
        return f"id:{self.id}, id_user: {self.id_user}, created_at: {self.created_at}, content:{self.content}"

    def _is_valid_id_user(self, id_user):
        regex = "^[0-9][0-9]*$"
        if not re.match(regex, id_user):
            raise ValueError("User id is not correct")
        return id_user

    def _is_valid_date_time(self, created_at):
        if not datetime.datetime.strptime(created_at, "%d-%m-%Y"):
            raise ValueError("Not a valid datetime")
        return created_at

    def _is_valid_content(self, content):
        if not len(content) <= 256:
            raise ValueError("Content cannot excede 256 characters.")
        return content
