from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship, validates
from tweets_demo.app import db
import re
from datetime import datetime
import ipdb


class Tweet(db.Model):
    from tweets_demo.models.comment import Comment

    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(String(255), nullable=False)
    content = Column(String(256), nullable=False)
    comments = relationship("Comment", primaryjoin="Tweet.id==Comment.id_tweet")

    def __init__(self, id_user="", created_at="", content=""):
        self.id_user = id_user
        self.created_at = created_at
        self.content = content

    def __repr__(self):
        return f"id:{self.id}, id_user: {self.id_user}, created_at: {self.created_at}, content:{self.content}"

    # def _is_valid_id_user(self, id_user):
    #     regex = "^[0-9][0-9]*$"
    #     if not re.match(regex, id_user):
    #         raise ValueError("User id is not correct")
    #     return id_user

    # def _is_valid_date_time(self, created_at):
    #     if not datetime.strptime(created_at, "%d-%m-%Y %H:%M"):
    #         raise ValueError("Not a valid datetime")
    #     # ipdb.set_trace()
    #     return created_at

    @validates(
        "content",
    )
    def validates_fields(self, key, value):
        if not getattr(self, "errors", None):
            self.errors = []

        if not value:
            self.errors.append(f"{key} is missing")

        if key == "content":
            if len(value) < 1:
                self.errors.append(f"{key} should have at least 1 character")
            if len(value) < 1:
                self.errors.append("Content cannot excede 256 characters.")

        return value

    def is_valid(self):
        return len(self.errors) == 0
