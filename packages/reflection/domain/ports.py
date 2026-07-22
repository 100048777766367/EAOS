from typing import Protocol

from packages.reflection.domain.models import ReflectionReport


class ReflectionRepository(Protocol):
    """Port Ä‘á»‹nh nghÄ©a cÃ¡c hÃ nh vi lÆ°u trá»¯ vÃ  truy váº¥n bÃ¡o cÃ¡o tá»± suy ngáº«m."""

    def save(self, report: ReflectionReport) -> ReflectionReport: ...

    def find_by_id(self, report_id: str) -> ReflectionReport | None: ...

    def find_by_subject(self, subject: str) -> list[ReflectionReport]: ...

