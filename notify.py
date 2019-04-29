from flask_restful import Resource
from flask import request
import queue
from functools import wraps

Q = queue.Queue(0)


def status():
    print(Q.queue)  # 查看队列中所有元素
    print(Q.qsize())  # 返回队列的大小
    print(Q.empty())  # 判断队空
    print(Q.full())  # 判断队满


def worker():
    while True:
        status()
        item = Q.get()
        if item is None:
            break
        do_work(item)
        Q.task_done()


def do_work(item):
    print(item)
    from ext import get_connect
    es = get_connect()
    if item['type'] == 'start':
        es.indices.create(index='moop-oplog', ignore=400)
        del item['type']
        es.index(index='moop-oplog', doc_type='moop', body=item)
    elif item['type'] == 'stop':
        try:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"tenant_id.keyword": item['tenant_id']}},
                            {"term": {"user_name.keyword": item['user_name']}},
                        ]
                    }
                },
                "sort": {"start": "desc"},
                "size": 1
            }
            result = es.search(index="moop-oplog", body=query)
            temp = result['hits']['hits']
            if temp:
                source = temp[0]['_source']
                _id = temp[0]['_id']
                source['last_activity'] = item['last_activity']
                source['end'] = item['end']
                es.update("moop-oplog", _id, doc_type='moop', body={"doc": source})
            else:
                pass
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
        request.json['type'] = 'start'
        # 放进队列
        Q.put(request.json)
        return {}


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
        request.json['type'] = 'stop'
        # 放进队列
        Q.put(request.json)
        return {}
