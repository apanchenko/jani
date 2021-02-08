import time, logging
from functools import wraps

from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

_log = logging.getLogger(__name__)
_bucket: str = ''
write_api = None

class monitor:
    @staticmethod
    def init(url: str,
             org: str,
             token: str,
             bucket: str) -> None:

        client = InfluxDBClient(url=url, org=org, token=token)

        global write_api
        write_api = client.write_api(write_options=SYNCHRONOUS)

        global _bucket
        _bucket = bucket
        _log.info(f'Monitor {url} {org} {token} {_bucket}')

    def __init__(self, granularity: int = 600):
        self._granularity: int = granularity
        self._count: int = 0
        self._duration: float = 0
        self._send_time: float = time.time() + self._granularity

    def __call__(self, fn):
        @wraps(fn)
        async def wrapper(*args, **kwds):
            # measure call
            ts = time.time()
            result = await fn(*args, **kwds)
            self._duration += time.time() - ts
            self._count += 1

            if ts > self._send_time:
                tps = self._count / self._granularity
                latency = self._duration / self._count
                # send data point
                write_api.write(
                    bucket = _bucket,
                    record = f'{fn.__name__} tps={tps},latency={latency}'
                )
                # reset counters
                self._duration = 0
                self._count = 0
                self._send_time = ts + self._granularity

            return result

        return wrapper
