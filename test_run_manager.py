#!/usr/bin/env python

from ping_test import PingTest
from run_manager import RunManager, LoggingResultManager, JsonlResultManager
from pprint import pprint

lrm = LoggingResultManager()
jrm = JsonlResultManager()
resman = jrm
rm = RunManager(interval=60, resman=resman, test_cls=PingTest, kwargs=dict(host='192.168.10.169'))
rm.start()
try:
    rm.join()
except KeyboardInterrupt:
    rm.stop()
    print("Stopping the RunManager... Please wait for the last run to complete or press Ctrl-C again.")
    try:
        rm.join()
    except KeyboardInterrupt:
        rm.kill()
