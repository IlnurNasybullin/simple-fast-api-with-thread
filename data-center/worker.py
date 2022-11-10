import time

class Worker:

    def __init__(self, lock, supplier, clear):
        self._lock = lock
        self._supplier = supplier
        self._clear = clear

    def start(self):
        while (True):
            self._lock.acquire()
            try:
                variable = self._supplier()
                if variable is not None:
                    self._clear()
                    print("global variable is cleaned!")
            finally:
                self._lock.release()

            if variable is None:
                time.sleep(5)
            else:
                self._do_something(variable)

    def _do_something(self, variable):
        print("execution!")
        time.sleep(15)
