#!/usr/bin/env python

import attr
import typing

@attr.s
class NumericalMetric():
    value: float = attr.ib()
    name: str = attr.ib()
    descr: str = attr.ib()

@attr.s
class PassFailTestResult():
    passed: bool = attr.ib()
    numerical_metrics: typing.List[NumericalMetric] = attr.ib(factory=list)
    #: contextual information (like the output lines used for outcome determination)
    debug_context: dict = attr.ib(factory=dict)

@attr.s
class Test():
    #: will be killed if not finished in time
    max_duration = attr.ib(default=60)
    def run(self):
        """ Returns TestResult """

@attr.s
class PassFailTest(Test):
    def run(self):
        """ Returns PassFailTestResult """
