"""Event Bus and Immutable Domain Event Definitions."""

import asyncio
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, TypeVar


@dataclass(frozen=True, slots=True, kw_only=True)
class DomainEvent:
    event_id: str
    topic: str
    correlation_id: str | None = None
    trace_id: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True, kw_only=True)
class KnowledgeCreatedEvent(DomainEvent):
    artifact_id: str
    title: str
    content: str
    author: str


@dataclass(frozen=True, slots=True, kw_only=True)
class ReflectionAnalyzedEvent(DomainEvent):
    report_id: str
    subject: str
    passed_checks: bool


@dataclass(frozen=True, slots=True, kw_only=True)
class ExperienceIngestedEvent(DomainEvent):
    experience_id: str
    reflection_id: str


@dataclass(frozen=True, slots=True, kw_only=True)
class PredictionRunEvent(DomainEvent):
    prediction_id: str
    risk_detected: bool


@dataclass(frozen=True, slots=True, kw_only=True)
class EvolutionProposedEvent(DomainEvent):
    evolution_id: str
    version: str


@dataclass(frozen=True, slots=True, kw_only=True)
class CapabilityHealthDegradedEvent(DomainEvent):
    capability_id: str
    current_health_score: float = 0.0
    drift_index: float = 0.0
    observed_latency_ms: float = 0.0
    coverage_percentage: float = 0.0
    broken_bindings: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True, kw_only=True)
class IncidentReportedEvent(DomainEvent):
    incident_id: str
    severity: str
    title: str = ""
    summary: str = ""


E = TypeVar("E", bound=DomainEvent)
EventHandler = Callable[[E], Coroutine[Any, Any, None]]


class EventBus:
    """Asynchronous reactive Event Mesh supporting topic subscriptions."""

    def __init__(self) -> None:
        self._handlers: dict[type[DomainEvent], list[EventHandler[Any]]] = {}

    def subscribe(self, event_type: type[E], handler: EventHandler[E]) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def publish(self, event: DomainEvent) -> None:
        event_type = type(event)
        handlers = self._handlers.get(event_type, [])
        if handlers:
            tasks = [handler(event) for handler in handlers]
            await asyncio.gather(*tasks, return_exceptions=False)
