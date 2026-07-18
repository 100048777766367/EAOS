from typing import Protocol

from packages.reflection.domain.models import ReflectionReport


class ReflectionRepository(Protocol):
    """Port định nghĩa các hành vi lưu trữ và truy vấn báo cáo tự suy ngẫm."""

    def save(self, report: ReflectionReport) -> ReflectionReport: ...

    def find_by_id(self, report_id: str) -> ReflectionReport | None: ...

    def find_by_subject(self, subject: str) -> list[ReflectionReport]: ...