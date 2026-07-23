"""Token Bucket rate limiting middleware for sensitive admin endpoints."""

import asyncio
import time
from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class RateLimitCheck(BaseModel):
    """Value object representing the result of a rate limit check."""

    model_config = ConfigDict(frozen=True)

    client_ip: str
    allowed: bool
    remaining_tokens: float


class TokenBucketRateLimiter:
    """Thread-safe Token Bucket rate limiter preventing DoS attacks."""

    _buckets: ClassVar[dict[str, dict[str, float]]] = {}

    def __init__(
        self,
        capacity: int = 10,
        refill_rate: float = 1.0,
    ) -> None:
        self.capacity: float = float(capacity)
        self.refill_rate: float = refill_rate
        self._lock = asyncio.Lock()

    async def allow_request(self, client_ip: str) -> RateLimitCheck:
        """Evaluates token bucket capacity with async lock protection."""
        async with self._lock:
            now = time.monotonic()

            if client_ip not in self._buckets:
                self._buckets[client_ip] = {
                    "tokens": self.capacity,
                    "last_refill": now,
                }

            bucket = self._buckets[client_ip]
            elapsed = now - bucket["last_refill"]
            bucket["tokens"] = min(
                self.capacity,
                bucket["tokens"] + elapsed * self.refill_rate,
            )
            bucket["last_refill"] = now

            if bucket["tokens"] >= 1.0:
                bucket["tokens"] -= 1.0
                return RateLimitCheck(
                    client_ip=client_ip,
                    allowed=True,
                    remaining_tokens=round(bucket["tokens"], 2),
                )

            return RateLimitCheck(
                client_ip=client_ip,
                allowed=False,
                remaining_tokens=round(bucket["tokens"], 2),
            )
