"""Bridge connecting OpenTelemetry metrics to dynamic architectural fitness rules."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class TelemetryFitnessFeedback(BaseModel):
    """Value object containing metric telemetry and generated fitness rule."""

    model_config = ConfigDict(frozen=True)

    metric_name: str
    observed_value: float
    dynamic_rule_generated: str


class TelemetryFitnessBridge:
    """Bridge translating telemetry observations into dynamic fitness functions."""

    def process_telemetry_trace(
        self,
        trace_metrics: dict[str, Any],
    ) -> TelemetryFitnessFeedback:
        """Generates dynamic fitness expression from observed telemetry metrics."""
        metric_name = str(trace_metrics.get("metric_name", "p99_latency_ms"))
        val = float(trace_metrics.get("value", 150.0))

        if "latency" in metric_name.lower():
            threshold = max(200.0, val * 1.2)
            rule_str = f"{metric_name} <= {threshold:.1f}"
        elif "error" in metric_name.lower():
            rule_str = f"{metric_name} <= 0.01"
        else:
            rule_str = f"{metric_name} >= 80.0"

        return TelemetryFitnessFeedback(
            metric_name=metric_name,
            observed_value=val,
            dynamic_rule_generated=rule_str,
        )
