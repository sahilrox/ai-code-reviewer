import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds

        # Clean old requests outside window
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > window_start
        ]

        if len(self.requests[key]) >= self.max_requests:
            return False

        self.requests[key].append(now)
        return True

    def get_remaining(self, key: str) -> int:
        now = time.time()
        window_start = now - self.window_seconds
        recent = [t for t in self.requests[key] if t > window_start]
        return max(0, self.max_requests - len(recent))

rate_limiter = RateLimiter()