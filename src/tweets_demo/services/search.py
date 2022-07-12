from flask import Flask, request

from tweets_demo.models.tweet import Tweet
from tweets_demo.models.comment import Comment
import ipdb


class SearchItem:
    def __init__(self):
        self.results = dict()

    def search(self, query=""):
        if self.results == dict():
            for model, attribute in self.searchable_models():
                self.results[model.__tablename__] = self._model_search(model, attribute, query)
        return self.results

    def searchable_models(self):
        return [(Tweet, "content"), (Comment, "content")]

    def _model_search(self, model, attribute, query):
        return model.query.filter(getattr(model, attribute).like("%" + query + "%")).all()
