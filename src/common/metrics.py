from prometheus_client import Counter, Summary, Gauge, Histogram, start_http_server
from typing import Optional
import threading

_metrics_started = False
_lock = threading.Lock()

REQS = Counter('req_total', 'Total requests', ['service','route','status'])
LAT = Histogram('latency_seconds', 'Request latency (s)', ['service','route'])
QPS = Gauge('qps_current', 'Instantaneous QPS', ['service','route'])
BATCH = Histogram('batch_size', 'Batch sizes', ['service','route'])

def ensure_metrics(port: int) -> None:
    global _metrics_started
    with _lock:
        if not _metrics_started:
            start_http_server(port)
            _metrics_started = True
