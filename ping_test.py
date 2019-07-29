#!/usr/bin/env python

from interfaces import PassFailTest, PassFailTestResult

# variant using subprocess
class PingTestSubprocess(PassFailTest):
    max_duration = 59

    def __init__(self, host):
        self.host = host
    def run(self):
        import subprocess
        import os
        process_result = subprocess.run('ping -c 8 ' + self.host, shell=True, stdout=subprocess.PIPE)
        passed = process_result.returncode == 0
        nm = []
        dc = {
          'output': process_result.stdout,
          'return_code': process_result.returncode
        }
        return PassFailTestResult(passed, numerical_metrics=nm, debug_context=dc)


### variant using pythonping
class PingTestPythonping(PassFailTest):
    max_duration = 60

    def __init__(self, host):
        self.host = host
    def run(self):
        from pythonping import ping
        from io import StringIO
        out = StringIO()
        passed = ping(self.host, verbose=True, out=out)
        print(repr(passed))
        nm = []
        dc = {'output': out}
        return PassFailTestResult(passed, numerical_metrics=nm, debug_context=dc)

PingTest = PingTestSubprocess
