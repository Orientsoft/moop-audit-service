#!/usr/bin/python
# -*- coding:utf-8 -*-
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
