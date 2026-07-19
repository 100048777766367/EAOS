from packages.self_rewrite.domain.models import SelfRewriteJob
from packages.self_rewrite.domain.ports import SelfRewriteRepository


class InMemorySelfRewriteRepository(SelfRewriteRepository):
    """Adapter lưu trữ kết quả Self Rewrite trong RAM phục vụ kiểm thử."""

    def __init__(self) -> None:
        self._store: dict[str, SelfRewriteJob] = {}

    def save(self, job: SelfRewriteJob) -> SelfRewriteJob:
        self._store[job.id] = job
        return job

    def find_by_id(self, job_id: str) -> SelfRewriteJob | None:
        return self._store.get(job_id)

    def list_all(self) -> list[SelfRewriteJob]:
        return list(self._store.values())
