#!/usr/bin/python
# -*- coding: utf-8 -*-
from app import app
from elasticsearch import Elasticsearch
from flask import g
from pymongo import MongoClient

def get_connect():
    with app.app_context():
        es = getattr(g, '_es', None)
        if es is None:
            es = g._es = Elasticsearch([app.config['ES_HOST']], http_auth=(app.config['ES_USER'], app.config['ES_PWD']),
                                       port=app.config['ES_PORT'])
        return es


def get_db():
    global connection
    if not app.config['MONGODB_URI']:
        connection = None
        return
    try:
        connection
    except NameError:
        connection = MongoClient(app.config['MONGODB_URI'])
    db = connection[app.config['MONGODB_NAME']]
    return db