import time
from dataclasses import dataclass

"""Token Bucket Rate Limiter for API Security."""


@dataclass
class RateLimitResult:
    """Rate limit evaluation result."""

    allowed: bool
    remaining_tokens: float


class TokenBucketRateLimiter:
    """In-memory Token Bucket Rate Limiter per IP address."""

    def __init__(self, capacity: float = 10.0, refill_rate: float = 1.0) -> None:
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets: dict[str, float] = {}
        self.last_update: dict[str, float] = {}

    async def allow_request(self, ip_address: str) -> RateLimitResult:
        """Evaluates whether an IP address is allowed to proceed."""
        now = time.time()
        last = self.last_update.get(ip_address, now)
        elapsed = now - last

        current_tokens = self.buckets.get(ip_address, self.capacity)
        current_tokens = min(self.capacity, current_tokens + elapsed * self.refill_rate)

        self.last_update[ip_address] = now

        if current_tokens >= 1.0:
            self.buckets[ip_address] = current_tokens - 1.0
            return RateLimitResult(allowed=True, remaining_tokens=self.buckets[ip_address])

        self.buckets[ip_address] = current_tokens
        return RateLimitResult(allowed=False, remaining_tokens=current_tokens)
