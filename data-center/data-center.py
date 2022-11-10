import threading

from fastapi import FastAPI

from worker import Worker

app = FastAPI()

variable = None
lock = threading.Lock()

def read_variable():
    global variable
    return variable

def clear_variable():
    global variable
    variable = None

worker = Worker(lock=lock, supplier=read_variable, clear=clear_variable)

t = threading.Thread(target=worker.start)
t.start()

@app.get("/calculate")
def calculate():
    global lock, variable

    lock.acquire()
    task_is_accepted = False
    try:
        is_not_executed = read_variable() is None
        if is_not_executed:
            print("thread is not executed!")
            variable = "execute!"
            task_is_accepted = True
    finally:
        lock.release()


    return {"task_is_accepted": task_is_accepted}