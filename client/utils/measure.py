"""
- measures function calls TPS and Latency
- reports to InfluxDB

TODO: align reports in time by period
TODO: set measurements accuracy

Usage:
    measure.init(...)

    @measured
    def do_something()
        ...
"""

import time, logging
from typing import Dict, Any
from functools import wraps

from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

_bucket:      str = ''
_write_api        = None
_granularity: int = 60
_send_time:   float
_records:     Dict[str, Any] = {}
_log           = logging.getLogger(__name__)


def init(url: str, org: str, token: str, bucket: str) -> None:
    """
    Initialize before any measured function called

    :param url: InfluxDB server API url
    :param org: organization name
    :param token: auth token
    :param bucket: destination bucket name
    """
    global _write_api
    global _bucket
    global _send_time
    client = InfluxDBClient(url=url, org=org, token=token)
    _write_api = client.write_api(write_options=SYNCHRONOUS)
    _bucket = bucket
    _send_time = time.time() + _granularity


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

    def linear(self, ts: float) -> str:
        if self.count == 0:
            return f'{self.label} tps={0},latency={0} {int(ts * 1000)}'

        tps = self.count / _granularity
        latency = self.duration / self.count
        self.count = 0
        self.duration = 0
        return f'{self.label} tps={tps},latency={latency} {int(ts * 1000)}'


def _report(mon: measured, ts: float) -> None:
    mon.count += 1
    mon.duration += time.time() - ts

    global _records
    _records[mon.label] = mon

    global _send_time
    if ts < _send_time:
        return

    records = [m.linear(ts) for label, m in _records.items()],
    _log.info('measured -------------->')
    _log.info(records)

    _write_api.write(bucket=_bucket, record=records, write_precision=WritePrecision.MS)

    _send_time = ts + _granularity
