"""Async Read-Write Lock Splay Cache Evictor for zero loop blocking."""

import asyncio
import time

from pydantic import BaseModel, ConfigDict


class EvictionResult(BaseModel):
    """Value object representing async batch cache eviction results."""

    model_config = ConfigDict(frozen=True)

    evicted_count: int
    remaining_nodes: int
    execution_time_ms: float


class AsyncRWLock:
    """True Reader-Writer Lock supporting concurrent reads and writer lock."""

    def __init__(self) -> None:
        self._readers: int = 0
        self._writer: bool = False
        self._cond = asyncio.Condition()

    async def acquire_read(self) -> None:
        """Acquires lock for reading. Allows concurrent readers."""
        async with self._cond:
            while self._writer:
                await self._cond.wait()
            self._readers += 1

    async def release_read(self) -> None:
        """Releases read lock."""
        async with self._cond:
            self._readers -= 1
            if self._readers == 0:
                self._cond.notify_all()

    async def acquire_write(self) -> None:
        """Acquires exclusive lock for writing."""
        async with self._cond:
            while self._writer or self._readers > 0:
                await self._cond.wait()
            self._writer = True

    async def release_write(self) -> None:
        """Releases exclusive write lock."""
        async with self._cond:
            self._writer = False
            self._cond.notify_all()


class AsyncRWLockSplayCache:
    """Splay Cache using true RWLock semantics for zero-block eviction."""

    def __init__(self, max_capacity: int = 1000) -> None:
        self.max_capacity: int = max_capacity
        self._cache: dict[str, str] = {f"key_{i}": f"val_{i}" for i in range(max_capacity + 200)}
        self._rwlock = AsyncRWLock()

    async def acquire_read(self, key: str) -> str | None:
        """Acquires non-blocking concurrent read access to cache key."""
        await self._rwlock.acquire_read()
        try:
            val = self._cache.get(key)
            if val is not None:
                self._cache[key] = self._cache.pop(key)
            return val
        finally:
            await self._rwlock.release_read()

    async def background_batch_evict(self) -> EvictionResult:
        """Executes LRU batch eviction under exclusive write lock."""
        start_time = time.perf_counter()

        await self._rwlock.acquire_write()
        try:
            total_items = len(self._cache)
            to_evict = max(0, total_items - self.max_capacity)

            if to_evict > 0:
                keys_to_remove = list(self._cache.keys())[:to_evict]
                for k in keys_to_remove:
                    self._cache.pop(k, None)

            remaining = len(self._cache)
            elapsed_ms = (time.perf_counter() - start_time) * 1000
        finally:
            await self._rwlock.release_write()

        return EvictionResult(
            evicted_count=to_evict,
            remaining_nodes=remaining,
            execution_time_ms=round(elapsed_ms, 3),
        )
