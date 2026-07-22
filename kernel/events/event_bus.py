import inspect
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    """Lớp cơ sở cho toàn bộ các Sự kiện Miền trong EAOS."""

    event_id: str
    topic: str = Field(default="system.general")
    correlation_id: str = Field(default="TX-NONE")
    trace_id: str = Field(default="TRC-NONE")
    sequence_number: int = Field(default=1)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class KnowledgeCreatedEvent(DomainEvent):
    """Sự kiện phát ra khi một tri thức mới được tạo lập."""

    artifact_id: str
    title: str
    content: str
    author: str


class ReflectionAnalyzedEvent(DomainEvent):
    """Sự kiện phát ra khi báo cáo tự chẩn đoán sự cố hoàn thành."""

    report_id: str
    subject: str
    passed_checks: bool


class ExperienceIngestedEvent(DomainEvent):
    """Sự kiện phát ra khi kinh nghiệm được nạp vào Knowledge Graph."""

    experience_id: str
    reflection_id: str


class PredictionRunEvent(DomainEvent):
    """Sự kiện phát ra khi hệ thống chẩn đoán dự báo thành công."""

    prediction_id: str
    risk_detected: bool


class EvolutionProposedEvent(DomainEvent):
    """Sự kiện phát ra khi đề xuất tự tiến hóa thích ứng được tạo lập."""

    evolution_id: str
    version: str


class EventBus:
    """Bộ điều phối Sự kiện Miền phi đồng bộ trung tâm của EAOS Kernel."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[[Any], Any]]] = {}
        self._history: list[DomainEvent] = []
        self._dlq: list[DomainEvent] = []

    def subscribe(
        self, event_type: type[DomainEvent], handler: Callable[[Any], Any]
    ) -> None:
        event_name = event_type.__name__
        self._handlers.setdefault(event_name, []).append(handler)

    async def publish(self, event: DomainEvent, max_retries: int = 3) -> None:
        event_name = event.__class__.__name__
        handlers = self._handlers.get(event_name, [])
        self._history.append(event)

        for handler in handlers:
            retries = 0
            success = False
            while retries < max_retries:
                try:
                    if inspect.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                    success = True
                    break
                except Exception as e:
                    retries += 1
                    print(
                        f"Retry {retries}/{max_retries} thất bại "
                        f"cho handler {handler.__name__}: {e}"
                    )

            if not success:
                self._dlq.append(event)
                print(f"Sự kiện {event.event_id} đã bị chuyển vào DLQ.")

    async def replay_topic(self, topic: str) -> list[DomainEvent]:
        matched_events = [e for e in self._history if e.topic == topic]
        ordered_events = sorted(matched_events, key=lambda x: x.sequence_number)

        for event in ordered_events:
            event_name = event.__class__.__name__
            handlers = self._handlers.get(event_name, [])
            for handler in handlers:
                if inspect.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
        return ordered_events

    def get_dlq(self) -> list[DomainEvent]:
        return self._dlq