from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery(
    "second_step",
    broker="redis://localhost:6379",
    backend="redis://localhost:6379",
    include=["second_step.tasks"]
)

app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    app.start()