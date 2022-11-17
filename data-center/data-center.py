import threading

from fastapi import FastAPI

from worker import Worker

app = FastAPI()

worker = Worker()

t = threading.Thread(target=worker.start)
t.start()

@app.get("/calculate")
def calculate():
    task_is_accepted = worker.try_submit_task(task="something task")
    return {"task_is_accepted": task_is_accepted}