from app import app
from elasticsearch import Elasticsearch
from flask import g


def get_connect():
    with app.app_context():
        es = getattr(g, '_es', None)
        if es is None:
            es = g._es = Elasticsearch([app.config['ES_HOST']], http_auth=(app.config['ES_USER'], app.config['ES_PWD']),
                                       port=app.config['ES_PORT'])
        return es
