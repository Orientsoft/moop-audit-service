# audit-service
audit service  
## 安装
pip install -r requirements.txt
## 启动命令
```python
python run.py
```
## api
```js
startInRequest
{
    "user_id": "fafadfadfa",
    "user_name": "wangbilin",
    "classroom_id": "fadfadfa",
    "classroom_name": "测试专题",
    "teacher_id": "laoshiid",
    "teacher_name": "laoshiname",
    "project_id": "projectid",
    "project_name": "projectname",
    "start": "2019-04-29T17:48:00",
    "namespace": "moop-dev",
    "tenant_id": "5cc026228c74b2d34997744d"
}
endInRequest
{
    "user_name": "wangbilin",
    "end": "2019-04-29T17:50:00",
    "last_activity":"2019-04-29T17:50:00",
    "tenant_id": "5cc026228c74b2d34997744d"
}
```
| method | path | query | request | response | remark |
| ------ | ---- | ----- | ------- | -------- | ------ |
| POST | /notify/end | ----- | endInRequest | {} | ------ |
| POST | /notify/start | ----- | startInRequest | {} | ------ |


## config.yaml
    config:
      #应用监听的ip
      HOST: '0.0.0.0'
      #应用的端口
      PORT: 7777
      #应用debug模式
      DEBUG: true
      #ES地址
      ES_HOST: '192.168.0.21'
      #ES用户名
      ES_USER: 'elastic'
      #ES密码
      ES_PWD: 'd2VsY29tZTEK'
      #ES端口
      ES_PORT: '9200'