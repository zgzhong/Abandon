# tasks.py
from __future__ import absolute_import
from celery_test.celery import app
import requests
import time

@app.task
def visit_url(url):
    req = requests.head(url)
    return req.status_code
