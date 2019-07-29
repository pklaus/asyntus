#!/usr/bin/env python

from ping_test import PingTest
from pprint import pprint

ping_winowl = PingTest(host='192.168.99.1')
testresult = ping_winowl.run()
# for now, we are not interested in the debug context...
testresult.debug_context = {}
pprint(testresult)
