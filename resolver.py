import multiprocessing as mp
import time

from app import task
from app.bus import Bus

from config import HOST, QUEUE, USER, PASSWORD
from config import MAXIMUM_PARALLEL, RESOLVER_TIMEOUT


def loop(func):
    def wrapper(self, *args, **kwargs):
        if self.timeout is not None:
            while True:
                func(self, *args, **kwargs)
                time.sleep(self.timeout)
        else:
            func(self, *args, **kwargs)
        return
    return wrapper


class Resolver(object):
    def __init__(self, timeout=RESOLVER_TIMEOUT,
                 max_parallel=MAXIMUM_PARALLEL):
        self.timeout = timeout
        self.available = max_parallel

    def update(self, result):
        Bus.update_task_in_db(result[0], **result[1])
        self.available += 1

    @loop
    def resolve(self):
        if self.available > 0:
            pool = mp.Pool(self.available)
            for i in range(self.available):
                t = Bus.get_task_from_queue(HOST, QUEUE, USER, PASSWORD)
                if t is not None:
                    pool.apply_async(task.run, args=(t, ),
                                     callback=self.update)
                    self.available -= 1
            pool.close()


def main():
    r = Resolver()
    r.resolve()

if __name__ == "__main__":
    main()
