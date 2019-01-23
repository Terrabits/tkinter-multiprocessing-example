import ctypes
import multiprocessing
import time

class Worker(object):
    def __init__(self, queue, message, time_s):
        self._is_alive = multiprocessing.Value(ctypes.c_bool, True)
        self.i         = 0
        self.queue     = queue
        self.message   = message
        self.time_s    = time_s

    def get_is_alive(self):
        with self._is_alive.get_lock():
            return self._is_alive.value
    def set_is_alive(self, value):
        with self._is_alive.get_lock():
            self._is_alive.value = value
    is_alive = property(get_is_alive, set_is_alive)

    def run(self):
        while True:
            # segmented sleep
            # check is_alive periodically
            SLEEP_TIME_S =  self.time_s
            LOOP_COUNT   = round(SLEEP_TIME_S / 0.1)
            for i in range(0, LOOP_COUNT):
                if not self.is_alive:
                    return
                else:
                    time.sleep(float(SLEEP_TIME_S) / LOOP_COUNT)
            # do work
            self.i += 1
            self.queue.put(f'i={self.i}: {self.message}')

class Process(object):
    def __init__(self, queue):
        self.worker  = None
        self.process = None
        self.queue   = queue
    def __delete__(self):
        self.stop()

    def start(self, message, time_s):
        self.stop()
        self.worker  = Worker(self.queue, message, time_s)
        self.process = multiprocessing.Process(target=self.worker.run)
        self.process.start()

    def stop(self):
        if self.is_alive:
            self.worker.is_alive = False
            self.process.join()
            self.worker  = None
            self.process = None
    def get_is_alive(self):
        return bool(self.worker and self.process)
    is_alive = property(get_is_alive)
