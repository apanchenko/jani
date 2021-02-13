"""
Performance measurement
- measures function calls: TPS and Latency
- reports to InfluxDB

Usage:
    measure.init(...)

    @measured
    def do_something()
        ...

TODO: tests
TODO: separate library
TODO: optionally report every period to support staked presentation
TODO: write pending output on shutdown
"""

import time, logging
from typing import Any, List, Callable, TypeVar, cast
from functools import wraps
from datetime import datetime as dt

from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

_bucket:    str
_delays:    int
_format:    str
_batch :    int
_influx:    Any
_log   :    logging.Logger
_out   :    List[str]

F = TypeVar("F", bound=Callable[..., Any]) 

def init(url: str,
         organ: str,
         token: str,
         bucket: str,
         delay: int = 1,
         latency_accuracy: int = 6,
         batch_size: int = 10) -> None:
    """
    Initialize before any measured function called

    url              : InfluxDB server API url
    organ            : InfluxDb organization
    token            : InfluxDb auth token
    bucket           : InfluxDb destination bucket
    delay            : minutes between consecutive reports
    latency_accuracy : number of digits after point for latency
    batch_size       : send records in batches of this size
    """
    global _influx, _bucket, _delays, _format, _batch, _out, _log
    client  = InfluxDBClient(url=url, org=organ, token=token)
    _influx = client.write_api(write_options=SYNCHRONOUS)
    _bucket = bucket
    _delays = delay * 60
    _format = f'.{latency_accuracy}f'
    _batch  = batch_size
    _out    = []
    _log    = logging.getLogger('⏱️')
    _log.info(f'Report measured calls every ' + ('minute' if delay == 1 else f'{delay} minutes'))

class measured:
    """
    Measure async function calls
    """
    count: int = 0
    spent: float = 0
    period: int = 0

    def __init__(self, label:str = None) -> None:
        self.label = label

    def __call__(self, fn: F) -> F:
        if self.label is None:
            self.label = fn.__name__

        @wraps(fn)
        async def wrapper(*args, **kwds):
            start = time.time()
            result = await fn(*args, **kwds)
            self._report(start)
            return result
        return cast(F, wrapper)

    def _report(self, start: float) -> None:
        finish = time.time()
        period = int(finish / _delays)

        #         D   C       B   A 
        # ------c-|---|---|---|-c-|------->
        #         p   0       0   p

        if period > self.period:
            global _out
            if self.count > 0:
                # write D
                _out.append(self._linear(self.period))

                if period > self.period + 1:
                    # write C
                    _out.append(self._empty(self.period + 1))
        
            if period > self.period + 2:
                # write B
                _out.append(self._empty(period - 1))

            if len(_out) >= _batch:
                #_log.info(f'output size {len(_out)}, write {_out[:_batch]}')
                _influx.write(bucket=_bucket, record=_out[:_batch], write_precision=WritePrecision.S)
                _out = _out[_batch:]
                #_log.info(f'{len(_out)} records went to next batch')

            self.period = period

        # save this call
        self.count += 1
        self.spent += finish - start
        #_log.info(f'{dt.fromtimestamp(period * _delays):%H:%M} {self.label} {format(finish - start, _format)}')

    def _empty(self, period: int) -> str:
        return f'{self.label} tps=0,latency=0 {period * _delays}'

    def _linear(self, period: int) -> str:
        tps = self.count / _delays
        latency = self.spent / self.count
        self.count = 0
        self.spent = 0
        return f'{self.label} tps={tps:.3f},latency={format(latency, _format)} {period * _delays}'
