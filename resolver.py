from datetime import datetime
import multiprocessing as mp
import time
import traceback
import logging

from app import task
from app.bus import Bus
from app import logger

from config import HOST, QUEUE, USER, PASSWORD
from config import RESOLVER_MAXIMUM_PARALLEL, RESOLVER_TIMEOUT
from config import RESOLVER_LOGFILE, RESOLVER_LOGLEVEL


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
                 max_parallel=RESOLVER_MAXIMUM_PARALLEL,
                 filelog=RESOLVER_LOGFILE,
                 loglevel=RESOLVER_LOGLEVEL):
        global log

        if "log" not in globals():
            if filelog is not None:
                log = logging.getLogger(__name__)
                log.addHandler(logger.FileHandler(filelog))
                log.setLevel(getattr(logging, loglevel))
            else:
                log = logging.getLogger(__name__)
                log.addHandler(logger.StreamHandler())
                log.setLevel(getattr(logging, loglevel))

        self.timeout = timeout
        self.available = max_parallel

    def update(self, result):
        try:
            Bus.update_task_in_db(result[0].id, **result[1])
            self.available += 1
            log.info("Task {} Complete".format(result[0].id))
        except:
            log.error(
                "Something wrong happend while db task update process\n{}".
                format(traceback.format_exc())
            )

    @loop
    def resolve(self):
        if self.available > 0:
            pool = mp.Pool(self.available)
            for i in range(self.available):
                t = Bus.get_task_from_queue(HOST, QUEUE, USER, PASSWORD)
                if t is not None:
                    Bus.update_task_in_db(t.id,
                        **{"status": "In process",
                           "start_time": datetime.utcnow()})
                    log.info("Task {} now In process".format(t.id))
                    pool.apply_async(task.run, args=(t, ),
                                     callback=self.update)
                    self.available -= 1
            pool.close()


def main():
    try:
        global log

        if RESOLVER_LOGFILE is not None:
            log = logging.getLogger(__name__)
            log.addHandler(logger.FileHandler(RESOLVER_LOGFILE))
            log.setLevel(getattr(logging, RESOLVER_LOGLEVEL))
        else:
            log = logging.getLogger(__name__)
            log.addHandler(logger.StreamHandler())
            log.setLevel(getattr(logging, RESOLVER_LOGLEVEL))

        r = Resolver()
        r.resolve()
    except KeyboardInterrupt:
        print('\nThe process was interrupted by the user')
        raise SystemExit

if __name__ == "__main__":
    main()
