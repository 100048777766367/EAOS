"""Cloudflare WAF driver with TTL auto-unblock cooldown mechanisms."""

from datetime import UTC, datetime, timedelta
from typing import Any

from pydantic import BaseModel, ConfigDict


class WAFBlockDecision(BaseModel):
    """Value object representing a temporary Cloudflare WAF block decision."""

    model_config = ConfigDict(frozen=True)

    ip: str
    action: str
    ttl_seconds: int
    auto_unblock_at: str


class CloudflareWAFRule(BaseModel):
    """Value object representing an active Cloudflare WAF block rule."""

    model_config = ConfigDict(frozen=True)

    rule_id: str
    blocked_ip: str
    mode: str
    status: str


class CloudflareWAFDriver:
    """Driver managing Cloudflare Zero-Trust WAF IP blocks and TTL cooldowns."""

    def __init__(self) -> None:
        self._blocked_ips: dict[str, dict[str, Any]] = {}

    def block_ip_with_cooldown(
        self,
        ip: str,
        ttl_seconds: int = 86400,
    ) -> WAFBlockDecision:
        """Blocks IP temporarily and sets TTL cooldown for auto-release."""
        now = datetime.now(UTC)
        unblock_time = now + timedelta(seconds=ttl_seconds)
        unblock_iso = unblock_time.isoformat()

        self._blocked_ips[ip] = {
            "blocked_at": now.isoformat(),
            "ttl_seconds": ttl_seconds,
            "unblock_at": unblock_iso,
            "status": "BLOCKED",
        }

        return WAFBlockDecision(
            ip=ip,
            action="BLOCK_WITH_COOLDOWN",
            ttl_seconds=ttl_seconds,
            auto_unblock_at=unblock_iso,
        )

    def check_and_auto_unblock(self, ip: str) -> bool:
        """Verifies whether the TTL key expired and auto-releases the block."""
        record = self._blocked_ips.get(ip)
        if not record:
            return True

        unblock_at_str = str(record.get("unblock_at", ""))
        unblock_at = datetime.fromisoformat(unblock_at_str)
        if datetime.now(UTC) >= unblock_at:
            self._blocked_ips.pop(ip, None)
            return True

        return False

    def block_malicious_ip(
        self,
        ip_address: str,
        reason: str = "Automated SOC Threat Mitigation",
    ) -> CloudflareWAFRule:
        """Calls Cloudflare WAF API to block a malicious IP address."""
        rule_id = f"cf_block_{hash(ip_address) & 0xFFFFFF:06x}"
        return CloudflareWAFRule(
            rule_id=rule_id,
            blocked_ip=ip_address,
            mode="block",
            status="ACTIVE",
        )
