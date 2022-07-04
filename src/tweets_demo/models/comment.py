from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship, validates
from tweets_demo.app import db


class Comment(db.Model):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    id_tweet = Column(Integer, ForeignKey=("tweet.id"), nullable=False)
    id_user = Column(Integer, ForeignKey=("user.id"), nullable=False)
    created_at = Column(String(255), nullable=False)
    content = Column(String(256), nullable=False)

    def __repr__(self):
        return f"id:{self.id}, id_tweet: {self.id_tweet}, id_user:{self.id_user},created_at: {self.created_at}, content:{self.content}"
