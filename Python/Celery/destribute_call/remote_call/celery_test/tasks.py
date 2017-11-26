from celery import Celery

app = Celery(
    broker="redis://127.0.0.1:6379/1", 
    backend="redis://127.0.0.1:6379/1", 
)

@app.task
def visit_url(url):
    pass
