"""
Performance measurement
- measures function calls: TPS and Latency
- reports to InfluxDB

Usage:
    measure.init(...)

    @measured
    def do_something()
        ...

TODO: report every period
TODO: batch reports
TODO: set measurements accuracy
TODO: optionally set label for any measured
TODO: tests
TODO: separate library
"""

import time, logging
from typing import Dict, Any
from functools import wraps

from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

_bucket:  str
_influx:  Any
_delay:   int
_period:  int = 0
_records: Dict[str, Any] = {}
_log      = logging.getLogger(__name__)


def init(url: str, org: str, token: str, bucket: str, delay_m: int = 1) -> None:
    """
    Initialize measures before any measured function called

    url     : InfluxDB server API url
    org     : organization name
    token   : auth token
    bucket  : destination bucket name
    delay_m : minutes between consecutive reports
    """
    global _influx, _bucket, _delay
    client = InfluxDBClient(url=url, org=org, token=token)
    _influx = client.write_api(write_options=SYNCHRONOUS)
    _bucket = bucket
    _delay = delay_m * 60
    _log.info(f'Measure every {delay_m} minute' + ('s' if delay_m > 1 else ''))


class measured:
    """
    Measure async function calls
    """
    label: str
    count: int = 0
    duration: float = 0

    def __call__(self, fn):
        self.label = fn.__name__
        @wraps(fn)
        async def wrapper(*args, **kwds):
            ts = time.time()
            result = await fn(*args, **kwds)
            _report(self, ts)
            return result

        return wrapper

    def linear(self, ts: str) -> str:
        if self.count == 0:
            return f'{self.label} tps={0},latency={0} {ts}'

        tps = self.count / _delay
        latency = self.duration / self.count
        self.count = 0
        self.duration = 0
        return f'{self.label} tps={tps},latency={latency} {ts}'


def _report(mon: measured, start: float) -> None:
    now = time.time()
    mon.count += 1
    mon.duration += now - start

    global _records, _period
    _records[mon.label] = mon

    period = int(now / _delay)
    if period <= _period:
        return

    _period = period

    ts = str(period * _delay)
    records = [m.linear(ts) for m in _records.values()]
    _log.info(records)

    _influx.write(bucket=_bucket, record=records, write_precision=WritePrecision.S)
