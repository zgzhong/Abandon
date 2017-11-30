from celery import Celery

app = Celery("own_task", broker="redis://127.0.0.1:6379/1", backend="redis://127.0.0.1:6379/1")

@app.task
def add(x, y):
    return x + y


if __name__ == "__main__":
    print(add.name)
    app.worker_main()
