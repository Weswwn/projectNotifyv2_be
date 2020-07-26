from projectNotifyv2_be.celery import app

@app.task
def hello_world():
    print('Hello world')