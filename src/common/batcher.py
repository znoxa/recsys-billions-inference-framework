import time, threading
from typing import Any, List, Callable, Tuple

class MicroBatcher:
    def __init__(self, max_size: int, max_delay_ms: int, process_fn: Callable[[List[Any]], List[Any]]):
        self.max_size = max_size
        self.max_delay_ms = max_delay_ms
        self.process_fn = process_fn
        self.lock = threading.Lock()
        self.cv = threading.Condition(self.lock)
        self.queue: List[Tuple[Any, threading.Event, int]] = []  # (item, done, idx)
        self.closed = False
        t = threading.Thread(target=self._loop, daemon=True)
        t.start()

    def submit(self, item: Any) -> Any:
        done = threading.Event()
        with self.lock:
            idx = len(self.queue)
            self.queue.append((item, done, idx))
            self.cv.notify_all()
        done.wait()
        return item.get('_result')  # type: ignore

    def _loop(self):
        while not self.closed:
            with self.lock:
                if not self.queue:
                    self.cv.wait(timeout=self.max_delay_ms / 1000.0)
                if not self.queue:
                    continue
                start = time.time()
                while (len(self.queue) < self.max_size) and ((time.time() - start) * 1000 < self.max_delay_ms):
                    self.cv.wait(timeout= (self.max_delay_ms/1000.0)/2)
                batch = self.queue[: self.max_size]
                self.queue = self.queue[self.max_size:]
            items = [i[0] for i in batch]
            results = self.process_fn(items)
            for (item, done, _), res in zip(batch, results):
                item['_result'] = res
                done.set()
