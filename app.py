from flask import Flask
from flask_restful import Api
import yaml
from applications.notify.api import Start, Stop
from applications.audit.api import Statistic,Detail
from multiprocessing import Pool
import os
import logging
import traceback

cpu_count = os.cpu_count()
app = Flask(__name__)
# 加载配置文件
with open('config.yaml', 'r', encoding='utf-8') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    for key, value in data.items():
        app.config[key] = value
# restful
api = Api(app)
api.add_resource(Start, '/notify/start')
api.add_resource(Stop, '/notify/end')
api.add_resource(Detail, '/student/stat')
api.add_resource(Statistic, '/project/stat')

app.config['pool'] = Pool(cpu_count)



@app.errorhandler(Exception)
def error_handler(error):
    logging.error('Request Error: {}\nStack: {}\n'.format(error, traceback.format_exc()))
    return 'AUDIT-SERVICE 未知错误', 500