from typing import Protocol

from packages.self_rewrite.domain.models import SelfRewriteJob


class SelfRewriteRepository(Protocol):
    """Port định nghĩa các hành vi lưu trữ và chẩn đoán Self Rewrite."""

    def save(self, job: SelfRewriteJob) -> SelfRewriteJob: ...

    def find_by_id(self, job_id: str) -> SelfRewriteJob | None: ...

    def list_all(self) -> list[SelfRewriteJob]: ...
