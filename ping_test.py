#!/usr/bin/env python

from interfaces import PassTest, PassTestResult, NumericalMetricValue

# variant using subprocess
class PingTestSubprocess(PassTest):
    max_duration = 59

    def __init__(self, host):
        self.host = host
    def run(self):
        import subprocess, re
        process_result = subprocess.run('ping -c 58 ' + self.host, shell=True, stdout=subprocess.PIPE)
        passed = process_result.returncode == 0
        output = process_result.stdout.decode('utf-8')
        total, received = None, None
        rt_min, rt_avg, rt_max, rt_stddev = None, None, None, None
        for line in output.split('\n'):
            if ' bytes from ' in line:
                pass # successful response line
            if 'Request timeout for icmp_seq' in line:
                pass # missing response line
            if 'packets transmitted' in line:
                # number of packets statistics line
                regex = r'(\d+) packets transmitted, (\d+) packets received, \d+\.\d+% packet loss'
                total, received = re.match(regex, line).groups()
            if 'round-trip min/avg/max/stddev = ' in line:
                # round trip statistics line
                regex = r'round-trip min\/avg\/max\/stddev = (\d+\.\d+)\/(\d+\.\d+)\/(\d+\.\d+)\/(\d+\.\d+) ms'
                rt_min, rt_avg, rt_max, rt_stddev = re.match(regex, line).groups()
        nm = [
          NumericalMetricValue('total', int(total)),
          NumericalMetricValue('received', int(received)),
          NumericalMetricValue('rt_min', float(rt_min)),
          NumericalMetricValue('rt_avg', float(rt_avg)),
          NumericalMetricValue('rt_max', float(rt_max)),
          NumericalMetricValue('rt_stddev', float(rt_stddev)),
        ]
        dc = {
          'output': output,
          'return_code': process_result.returncode
        }
        result = PassTestResult(passed, numerical_metrics=nm, debug_context=dc)
        return result


### variant using pythonping
class PingTestPythonping(PassTest):
    max_duration = 59

    def __init__(self, host):
        self.host = host
    def run(self):
        from pythonping import ping
        from io import StringIO
        out = StringIO()
        passed = ping(self.host, verbose=True, out=out)
        #print(repr(passed))
        nm = []
        dc = {'output': out}
        return PassTestResult(passed, numerical_metrics=nm, debug_context=dc)

### the default choice is:
PingTest = PingTestSubprocess
