from __future__ import absolute_import
from celery import Celery

app = Celery(
    "celery_test", 
    broker="redis://127.0.0.1:6379/1", 
    backend="redis://127.0.0.1:6379/1", 
    include=["celery_test.tasks"]
)
