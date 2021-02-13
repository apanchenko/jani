"""
Performance measurement
    - measures function calls: TPS and Latency
    - reports to InfluxDB

Usage:
    measure.init(...)

    @measured(...)
    def do_something()
        ...

TODO: raise when called before initialized
TODO: tests
TODO: separate library
TODO: write pending output on shutdown
"""

import time, logging
from typing import Any, List, Callable, TypeVar, cast
from functools import wraps
from datetime import datetime as dt

from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

F = TypeVar("F", bound=Callable[..., Any]) 

def init(url: str,
         organ: str,
         token: str,
         bucket: str,
         *,
         delay = 1,
         latency_accuracy = 6,
         batch_size = 10) -> None:
    """ Initialize before any measured function called
    url              : InfluxDB server API url
    organ            : InfluxDb organization
    token            : InfluxDb auth token
    bucket           : InfluxDb destination bucket
    delay            : minutes between consecutive reports
    latency_accuracy : number of digits after point for latency
    batch_size       : minimum number of records in batch to send
    sparse           : send record when measured, not every period
    """
    global _influx, _bucket, _delays, _format, _batch, _out, _log, _period
    _log    = logging.getLogger('⏱️')
    _log.info(f'Report measured calls every ' + ('minute' if delay == 1 else f'{delay} minutes'))
    _client  = InfluxDBClient(url=url, org=organ, token=token)
    _influx = _client.write_api(write_options=SYNCHRONOUS)
    _bucket = bucket
    _delays = delay * 60
    _format = f'.{latency_accuracy}f'
    _batch  = batch_size
    _out    = []
    _period = int(time.time() / _delays)


_bucket:    str
_delays:    int
_format:    str
_batch :    int
_influx:    Any
_log   :    logging.Logger
_out   :    List[str]
_decors:    List[Any] = []
_period:    int

class measured:
    """ Measure async function calls
    """
    count: int = 0      # number of calls
    spent: float = 0    # seconds spent in call
    period: int = 0     # for sparse measurements 

    def __init__(self, label:str=None, dense:bool=True) -> None:
        self._label = label
        self._dense = dense
        if dense:
            global _decors
            _decors.append(self)

    def __call__(self, fn: F) -> F:
        # use function name as label by default
        if self._label is None:
            self._label = fn.__name__    
        # select reporting strategy
        report = self._report_dense if self._dense else self._report_sparse

        @wraps(fn)
        async def wrapper(*args, **kwds):
            start = time.time()
            result = await fn(*args, **kwds)
            report(start)
            return result
        return cast(F, wrapper)

    def _report_sparse(self, start: float) -> None:
        finish = time.time()
        period = int(finish / _delays)

        #         D   C       B   A 
        # ------c-|---|---|---|-c-|------->
        #         p   0       0   p

        global _out
        if period > self.period:
            if self.count > 0:
                # write D
                ts = self.period * _delays
                _out.append(self._linear(ts))

                if period > self.period + 1:
                    # write C
                    ts = (self.period + 1) * _delays
                    _out.append(self._empty(ts))
        
            if period > self.period + 2:
                # write B
                ts = (period - 1) * _delays
                _out.append(self._empty(ts))

            self.period = period

            if len(_out) >= _batch:
                _log.info(f'output size {len(_out)}, write {_out}')
                _influx.write(bucket=_bucket, record=_out, write_precision=WritePrecision.S)
                _out.clear()

        # save this call
        self.count += 1
        self.spent += finish - start
        _log.info(f'report {self.label} {format(finish - start, _format)} at {dt.fromtimestamp(period * _delays):%H:%M}')

    def _report_dense(self, start: float) -> None:
        finish = time.time()
        period = int(finish / _delays)

        global _out, _period, _decors
        if period > _period:
            while period > _period:
                _log.info(f'work on {len(_decors)=}, {_period=}')
                sec = _period * _delays
                for d in _decors:
                    _out.append(d._empty(sec) if d.count==0 else d._linear(sec))
                _period += 1

            if len(_out) >= _batch:
                _log.info(f'output size {len(_out)}, write {_out}')
                _influx.write(bucket=_bucket, record=_out, write_precision=WritePrecision.S)
                _out.clear()

        # save this call
        self.count += 1
        self.spent += finish - start
        _log.info(f'report {self._label} {format(finish - start, _format)} at {dt.fromtimestamp(period * _delays):%H:%M}')

    def _empty(self, ts: int) -> str:
        return f'{self._label} tps=0,latency=0 {ts}'

    def _linear(self, ts: int) -> str:
        tps = self.count / _delays
        latency = self.spent / self.count
        self.count = 0
        self.spent = 0
        return f'{self._label} tps={tps:.3f},latency={format(latency, _format)} {ts}'
