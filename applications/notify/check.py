#!/usr/bin/python
# -*- coding:utf-8 -*-
from functools import wraps
from flask import request


def check_start(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        needed = ['user_id', 'user_name', 'classroom_id', 'classroom_name', 'teacher_id', 'teacher_name', 'project_id',
                  'project_name', 'start', 'namespace', 'tenant_id']
        for n in needed:
            if n not in request.json:
                return {
                    'error': '{} is not found'.format(n)
                }
        return f(*args, **kwargs)

    return decorated


def check_stop(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        needed = ['user_name', 'tenant_id', 'last_activity', 'end']
        for n in needed:
            if n not in request.json:
                return {
                    'error': '{} is not found'.format(n)
                }
        return f(*args, **kwargs)

    return decorated
