from flask import Flask
from flask_restful import Api
import yaml
from applications.notify.api import Start, Stop, worker

app = Flask(__name__)
# 加载配置文件
with open('config.yaml', 'r', encoding='utf-8') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    for key, value in data['config'].items():
        app.config[key] = value
# restful
api = Api(app)
api.add_resource(Start, '/notify/start')
api.add_resource(Stop, '/notify/end')


def config_daily_task():
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(worker, 'cron', minute='*/1', max_instances=2)
    scheduler.start()


config_daily_task()
