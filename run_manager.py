#!/usr/bin/env python

from multiprocessing import Process, Lock, Event, Pipe
import logging, time
import attr

from interfaces import ResultManager


logging.basicConfig(level='DEBUG')

class LoggingResultManager(ResultManager):

    def __init__(self, logger=None, name='resman', level='INFO'):
        self.level = level
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(name)
            self.logger.setLevel(level)

    def new_result(self, result):
        self.logger.log(self.logger.level, str(result))
        print("hi")


class JsonlResultManager(ResultManager):
    def __init__(self, filename='resman.jsonl'):
        import json
        self.filename = filename
    def filter(self, result):
        # for now, we are not interested in the debug context...
        result.debug_context = {}
    def new_result(self, result):
        self.filter(result)
        import json
        with open(self.filename, 'a+') as f:
            f.write(json.dumps({'ts': time.time(), 'result': attr.asdict(result)})+'\n')


class KillAfterTimeout():
    def __init__(self, timeout, target, args=(), kwargs={}):
        self.timeout = timeout
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self._running = Lock()
        self._process = None
        self._result = None

    def get_result(self):
        return self._result

    def run(self):
        self._running.acquire()
        recv_end, send_end = Pipe(False)
        def worker(send_end):
            result = self.target(*self.args, **self.kwargs)
            send_end.send(result)
        p = Process(target=worker, args=(send_end,))
        self._process = p
        p.start()
        p.join(timeout=self.timeout)
        if p.is_alive():
            p.kill()
            logging.error('process was running for too long, had to be killed...')
        else:
            self._result = recv_end.recv()
        self._running.release()


class RunManager():
    def __init__(self, test_cls, resman: ResultManager, args=(), kwargs={}, interval=60):
        self.test_cls = test_cls
        self.args = args
        self.kwargs = kwargs
        self.interval = interval
        self.resman = resman
        self._tolerance = 0.1
        self._timeout = interval - 0.1
        self._stop = Event()
        
    def run_until_timout_or_kill(self):
        test = self.test_cls(*self.args, **self.kwargs)
        kat = KillAfterTimeout(timeout=test.max_duration, target=test.run)
        kat.run()
        return kat.get_result()

    def start(self):
        def worker():
            start = time.time()
            while True:
                if self._stop.is_set(): break
                result = self.run_until_timout_or_kill()
                if self.resman:
                    self.resman.new_result(result)
                remaining_time = (start + self.interval) - time.time()
                logging.debug('remaining time: %f', remaining_time)
                if remaining_time > -self._tolerance:
                    if remaining_time > 0:
                        time.sleep(remaining_time)
                    start += self.interval
                else:
                    logging.error('The last test cycle took longer than expected (was the CPU suspended?). time drift of %f', remaining_time)
                    start = time.time()
        p = Process(target=worker)
        self._process = p
        p.start()

    def join(self):
        self._process.join()

    def stop(self):
        self._stop.set()

    def kill(self):
        self._process.kill()
