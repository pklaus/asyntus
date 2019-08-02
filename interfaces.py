#!/usr/bin/env python

import attr
import typing

@attr.s
class NumericalMetricValue():
    id: str = attr.ib()
    value: float = attr.ib()

@attr.s
class NumericalMetric():
    id: str = attr.ib()
    name: str = attr.ib()
    descr: str = attr.ib()

@attr.s
class PassTestResult():
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
class PassTest(Test):
    def run(self):
        """ Returns PassFailTestResult """
