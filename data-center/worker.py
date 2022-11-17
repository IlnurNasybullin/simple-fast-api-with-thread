import threading
import time


class Worker:

    def __init__(self):
        self._lock = threading.Lock()
        self._task = None

    def _read_task(self):
        self._lock.acquire()
        local_task = self._task
        self._lock.release()
        return local_task

    def try_submit_task(self, task):
        is_submitted = False

        self._lock.acquire()
        local_task = self._task
        if local_task is None:
            local_task = task
            self._task = local_task
            is_submitted = True
        self._lock.release()
        return is_submitted

    def _clear(self):
        self._lock.acquire()
        self._task = None
        self._lock.release()

    def start(self):
        while (True):
            local_task = self._read_task()
            if local_task is not None:
                self._clear()
                print("task is cleaned!")
                self._do_something(local_task)
            else:
                time.sleep(5)

    def _do_something(self, task):
        print("execution!")
        time.sleep(15)
