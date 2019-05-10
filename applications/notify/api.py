#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask_restful import Resource
from flask import request
import datetime
import logging
from applications.notify.check import check_start, check_stop
from applications.notify.work import do_work


class Start(Resource):
    @check_start
    def post(self):
        from app import app
        try:
            request.json['type'] = 'start'
            request.json['start'] = datetime.datetime.strptime(request.json['start'], '%Y-%m-%dT%H:%M:%S.%f')
            app.config['pool'].apply_async(do_work, (request.json,))
            return {}
        except:
            return '数据错误', 400


class Stop(Resource):
    @check_stop
    def post(self):
        from app import app
        try:
            request.json['type'] = 'stop'
            request.json['end'] = datetime.datetime.strptime(request.json['end'], '%Y-%m-%dT%H:%M:%S.%f')
            request.json['last_activity'] = datetime.datetime.strptime(request.json['last_activity'],
                                                                       '%Y-%m-%dT%H:%M:%S.%f')
            app.config['pool'].apply_async(do_work, (request.json,))
            return {}
        except Exception as e:
            logging.error(e)
            return '数据错误', 400
