import time
from celery import Celery


BROKER = "redis://localhost:6379/0"
BACKEND = "redis://localhost:6379/0"

app = Celery('tasks')
app.config_from_object("celeryconfig")

@app.task
def add(x, y):
    time.sleep(5)
    return x + y