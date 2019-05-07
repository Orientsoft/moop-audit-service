from flask_restful import Resource
from flask import request
from functools import wraps
import datetime

def do_work(item):
    print(item)
    from ext import get_connect, get_db
    es = get_connect()
    db = get_db()
    if item['type'] == 'start':
        del item['type']
        # save to mongodb
        db.oplog.insert(item)
        # save to es
        month = datetime.datetime.now().strftime('%Y-%m')
        index = 'moop-oplog-{}'.format(month)
        del item['_id']
        es.index(index=index, doc_type='moop', body=item)
    elif item['type'] == 'stop':
        try:
            # update mongodb
            result = db.oplog.find(
                {'tenant_id': item['tenant_id'], 'user_name': item['user_name'], 'end': {'$exists': False}}).sort(
                [('start', -1)]).limit(1)
            if result:
                for r in result:
                    _id = r['_id']
                db.oplog.update({'_id': _id},
                                {'$set': {'end': item['end'], 'last_activity': item['last_activity']}})
            else:
                print('start not found or end is writed')

            # save to es
            month = datetime.datetime.now().strftime('%Y-%m')
            index = 'moop-oplog-{}'.format(month)
            del item['type']
            es.index(index=index, doc_type='moop', body=item)
        except Exception as e:
            print(e)
    else:
        print('error data')


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


class Start(Resource):
    @check_start
    def post(self):
        from app import app
        try:
            request.json['type'] = 'start'
            request.json['start'] = datetime.datetime.strptime(request.json['start'],'%Y-%m-%dT%H:%M:%S.%f')
            app.config['pool'].apply_async(do_work, (request.json,))
            return {}
        except:
            return '数据错误',400


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


class Stop(Resource):
    @check_stop
    def post(self):
        from app import app
        try:
            request.json['type'] = 'stop'
            request.json['end'] = datetime.datetime.strptime(request.json['end'], '%Y-%m-%dT%H:%M:%S.%f')
            request.json['last_activity'] = datetime.datetime.strptime(request.json['last_activity'], '%Y-%m-%dT%H:%M:%S.%f')
            app.config['pool'].apply_async(do_work, (request.json,))
            return {}
        except:
            return '数据错误', 400
