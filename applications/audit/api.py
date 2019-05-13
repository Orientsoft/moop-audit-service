#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask_restful import Resource
from flask import request, jsonify


class Statistic(Resource):
    def get(self):
        classroom_id = request.args.get('classroom_id')
        tenant_id = request.args.get('tenant_id')
        from ext import get_db
        db = get_db()
        # 项目使用情况
        project = db.oplog.aggregate([
            {'$match': {'classroom_id': classroom_id, 'tenant_id': tenant_id}},
            {'$project': {'project_id': 1, 'diff': {'$subtract': ['$end', '$start']}}},
            {'$group': {'_id': '$project_id',
                        'count': {'$sum': 1},
                        'usetime': {'$sum': '$diff'}
                        }
             }
        ])
        projectinfo = {}
        for p in project:
            projectinfo[p['_id']] = int(p['usetime'] / 1000 / 60 / p['count'])
        print(projectinfo)
        # 学生使用情况
        result = db.oplog.aggregate([
            {'$match': {'classroom_id': classroom_id, 'tenant_id': tenant_id}},
            {'$project': {'user_id': 1, 'project_id': 1, 'project_name': 1, 'diff': {'$subtract': ['$end', '$start']}}},
            {'$group': {'_id': {'user_id': '$user_id', 'project_id': '$project_id', 'project_name': '$project_name'},
                        'count': {'$sum': 1},
                        'usetime': {'$sum': '$diff'}
                        }
             }
        ])
        returnObj = {}
        for r in result:
            user_id = r['_id']['user_id']
            project_id = r['_id']['project_id']
            project_avg = projectinfo[project_id]
            project_name = r['_id']['project_name']
            count = int(r['count'])
            usetime = int(r['usetime'] / 1000 / 60 )
            if user_id not in returnObj:
                returnObj[user_id] = {
                    'count': count,
                    'totaltime': usetime,
                    'chart': {
                        'x': [project_name],
                        'y1': [usetime],
                        'y2': [project_avg]
                    }
                }
            else:
                returnObj[user_id]['count'] += count
                returnObj[user_id]['totaltime'] += usetime
                returnObj[user_id]['chart']['x'].append(project_name)
                returnObj[user_id]['chart']['y1'].append(usetime)
                returnObj[user_id]['chart']['y2'].append(project_avg)
        return returnObj