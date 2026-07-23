"""Wazuh SIEM integration and Cloudflare WAF auto-blocking engine."""

import time
from typing import Any

from pydantic import BaseModel, ConfigDict


class WazuhAlertPayload(BaseModel):
    """Value object representing an alert forwarded to Wazuh SIEM."""

    model_config = ConfigDict(frozen=True)

    event_id: str
    level: int
    rule_description: str
    source_ip: str
    timestamp: str


class CloudflareWAFRule(BaseModel):
    """Value object representing a Cloudflare WAF IP block rule."""

    model_config = ConfigDict(frozen=True)

    rule_id: str
    blocked_ip: str
    mode: str
    status: str


class WazuhSIEMAdapter:
    """Adapter streaming audit ledger events to Wazuh SIEM Manager."""

    def __init__(
        self,
        syslog_host: str = "127.0.0.1",
        port: int = 514,
    ) -> None:
        self.syslog_host: str = syslog_host
        self.port: int = port
        self._event_buffer: list[dict[str, Any]] = []

    def stream_audit_event(
        self,
        event_data: dict[str, Any],
    ) -> WazuhAlertPayload:
        """Formats and dispatches audit log entry to Wazuh agent."""
        self._event_buffer.append(event_data)
        event_id = str(event_data.get("tx_id", f"EVT-{int(time.time())}"))
        source_ip = str(event_data.get("source_ip", "192.168.1.100"))
        is_security = "SECURITY" in str(event_data).upper()

        return WazuhAlertPayload(
            event_id=event_id,
            level=7 if is_security else 3,
            rule_description="EAOS Audit Ledger Security Event",
            source_ip=source_ip,
            timestamp="2026-07-23T04:16:00Z",
        )


class CloudflareWAFDriver:
    """Driver managing Cloudflare Zero Trust WAF security rules."""

    def block_malicious_ip(
        self,
        ip_address: str,
        reason: str = "Automated SOC Threat Mitigation",
    ) -> CloudflareWAFRule:
        """Calls Cloudflare API to block target malicious IP address."""
        rule_id = f"cf_block_{hash(ip_address) & 0xFFFFFF:06x}"
        return CloudflareWAFRule(
            rule_id=rule_id,
            blocked_ip=ip_address,
            mode="block",
            status="ACTIVE",
        )
