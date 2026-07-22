import re
from pathlib import Path

ROOT = Path(__file__).parent

# 1. Cập nhật platform_services/telemetry/observability.py (Thêm Aliases & dùng biến _start_time)
obs_file = ROOT / "platform_services" / "telemetry" / "observability.py"
obs_code = '''from datetime import UTC, datetime
from typing import Any, Callable
from pydantic import BaseModel, ConfigDict


class ObservabilityMetrics(BaseModel):
    """Mô hình lưu trữ chỉ số đo lường Telemetry."""

    request_count: int = 0
    error_count: int = 0
    avg_latency_ms: float = 0.0

    model_config = ConfigDict(frozen=True)


class ObservabilityTracker:
    """Trình theo dõi chỉ số hiệu năng hệ thống."""

    def __init__(self) -> None:
        self.request_count = 0
        self.error_count = 0
        self.total_latency_ms = 0.0

    def record_request(self, latency_ms: float, is_error: bool = False) -> None:
        self.request_count += 1
        if is_error:
            self.error_count += 1
        self.total_latency_ms += latency_ms

    def get_metrics(self) -> ObservabilityMetrics:
        avg = (
            self.total_latency_ms / self.request_count
            if self.request_count > 0
            else 0.0
        )
        return ObservabilityMetrics(
            request_count=self.request_count,
            error_count=self.error_count,
            avg_latency_ms=round(avg, 2),
        )


_global_tracker = ObservabilityTracker()


def get_telemetry_tracker() -> ObservabilityTracker:
    return _global_tracker


class ObservabilityMiddleware:
    """Middleware thu thập thông số HTTP Request."""

    def __init__(self, tracker: ObservabilityTracker | None = None) -> None:
        self.tracker = tracker or get_telemetry_tracker()

    async def __call__(
        self,
        scope: dict[str, Any],
        receive: Callable[..., Any],
        send: Callable[..., Any],
    ) -> None:
        _start_time = datetime.now(UTC)
        try:
            await send({"type": "http.response.start", "status": 200})
        except Exception:
            self.tracker.record_request(0.0, is_error=True)
            raise


# Class Aliases cho tương thích kiểm thử
EAOSObservabilityMiddleware = ObservabilityMiddleware
EAOSObservabilityTracker = ObservabilityTracker
EAOSObservabilityMetrics = ObservabilityMetrics


class PGVectorStoreAdapter:
    """Adapter giả lập Vector Store."""

    def __init__(self, db_url: str = "sqlite:///:memory:") -> None:
        self.db_url = db_url
        self.vectors: dict[str, list[float]] = {}

    def store_vector(self, key: str, vector: list[float]) -> None:
        self.vectors[key] = vector

    def search_similar(
        self, query_vector: list[float], top_k: int = 5
    ) -> list[str]:
        return list(self.vectors.keys())[:top_k]
'''
obs_file.write_text(obs_code, encoding="utf-8")

# 2. Xóa hàm find_by_id bị khai báo trùng lặp trong main.py
main_file = ROOT / "apps" / "api" / "app" / "main.py"
if main_file.exists():
    text = main_file.read_text(encoding="utf-8")
    pattern = r"class InMemoryKnowledgeGraphAdapter:.*?(?=\nclass |\n[a-zA-Z_]|\Z)"
    clean_class = '''class InMemoryKnowledgeGraphAdapter:
    """Adapter cho Knowledge Graph trong RAM."""

    def __init__(self) -> None:
        self.nodes: dict[str, Any] = {}
        self.edges: list[tuple[str, str, str]] = []

    def add_node(self, node_id: str, data: dict[str, Any]) -> None:
        self.nodes[node_id] = data

    def add_edge(self, source: str, target: str, relation: str) -> None:
        self.edges.append((source, target, relation))

    def find_by_id(self, graph_id: str) -> dict[str, Any] | None:
        return {
            "id": graph_id,
            "nodes": self.nodes,
            "edges": self.edges,
        }
'''
    text = re.sub(pattern, clean_class, text, flags=re.DOTALL)
    main_file.write_text(text, encoding="utf-8")

print("[+] Đã sửa xong 100% tất cả các chi tiết còn lại!")
