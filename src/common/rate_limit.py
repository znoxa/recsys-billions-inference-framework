import time, threading

class TokenBucket:
    def __init__(self, rate_per_s: float, burst: int):
        self.rate = rate_per_s
        self.capacity = burst
        self.tokens = burst
        self.lock = threading.Lock()
        self.ts = time.time()

    def allow(self, cost: float = 1.0) -> bool:
        with self.lock:
            now = time.time()
            self.tokens = min(self.capacity, self.tokens + (now - self.ts) * self.rate)
            self.ts = now
            if self.tokens >= cost:
                self.tokens -= cost
                return True
            return False
