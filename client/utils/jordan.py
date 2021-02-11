"""
Performance measurement
- measures function calls: TPS and Latency
- reports to InfluxDB

Usage:
    measure.init(...)

    @measured
    def do_something()
        ...

TODO: batch reports
TODO: optionally set label for any measured
TODO: tests
TODO: separate library
TODO: optionally report every period to support staked presentation
"""

import time, logging
from typing import Any, List
from functools import wraps
from datetime import datetime as dt

from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

_influx:    Any
_bucket:    str
_delays:    int
_format:    str
_log        = logging.getLogger('⏱️')


def init(url: str, org: str, token: str, bucket: str, delay: int = 1, latency_accuracy: int = 6) -> None:
    """
    Initialize before any measured function called

    url              : InfluxDB server API url
    org              : InfluxDb organization
    token            : InfluxDb auth token
    bucket           : InfluxDb destination bucket
    delay            : minutes between consecutive reports
    latency_accuracy : number of digits after point for latency
    """
    global _influx, _bucket, _delays, _format
    client = InfluxDBClient(url=url, org=org, token=token)
    _influx = client.write_api(write_options=SYNCHRONOUS)
    _bucket = bucket
    _delays = delay * 60
    _format = f'.{latency_accuracy}f'
    _log.info(f'Measure every {delay} minute' + ('s' if delay > 1 else ''))


class measured:
    """
    Measure async function calls
    """
    label: str
    count: int = 0
    spent: float = 0
    period: int = 0

    def __call__(self, fn):
        self.label = fn.__name__
        @wraps(fn)
        async def wrapper(*args, **kwds):
            start = time.time()
            result = await fn(*args, **kwds)
            _report(self, start)
            return result

        return wrapper

    def _empty(self, period: int) -> str:
        return f'{self.label} tps=0,latency=0 {period * _delays}'

    def _linear(self, period: int) -> str:
        tps = self.count / _delays
        latency = self.spent / self.count
        self.count = 0
        self.spent = 0
        return f'{self.label} tps={tps:.3f},latency={format(latency, _format)} {period * _delays}'


def _report(m: measured, start: float) -> None:
    finish = time.time()
    period = int(finish / _delays)

    #         D   C       B   A 
    # ------c-|---|---|---|-c-|------->
    #         p   0       0   p

    out: List[str] = []

    if period > m.period:
        if m.count > 0:
            # write D
            out.append(m._linear(m.period))

            if period > m.period + 1:
                # write C
                out.append(m._empty(m.period + 1))
    
        if period > m.period + 2:
            # write B
            out.append(m._empty(period - 1))

        if len(out) > 0:
            #_log.info(f'write {out}')
            _influx.write(bucket=_bucket, record=out, write_precision=WritePrecision.S)

    # save this call
    m.count += 1
    m.spent += finish - start
    m.period = period
    #_log.info(f'{dt.fromtimestamp(period * _delays):%H:%M} {m.label} {format(finish - start, _format)}')
