from packages.reflection.domain.models import ReflectionReport
from packages.reflection.domain.ports import ReflectionRepository


class InMemoryReflectionRepository(ReflectionRepository):
    """Adapter lưu trữ báo cáo tự suy ngẫm trong RAM phục vụ kiểm thử."""

    def __init__(self) -> None:
        self._store: dict[str, ReflectionReport] = {}

    def save(self, report: ReflectionReport) -> ReflectionReport:
        self._store[report.id] = report
        return report

    def find_by_id(self, report_id: str) -> ReflectionReport | None:
        return self._store.get(report_id)

    def find_by_subject(self, subject: str) -> list[ReflectionReport]:
        return [r for r in self._store.values() if r.subject == subject]
